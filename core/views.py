from django.shortcuts import render
from .forms import DorkForm
from .models import Dork
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
import time
import random
import csv
import json

def detect_risk(link):
    risk_keywords = ["password", "admin", "login", "backup", "confidential"]
    filetypes = ["pdf", "doc", "docx", "xls", "xlsx", "csv"]

    risk_level = ""
    if any(ft in link for ft in filetypes):
        risk_level = "Fichier exposé"
    if any(rk in link.lower() for rk in risk_keywords):
        risk_level = "Risque élevé"
    return risk_level


def get_google_results(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    url = f"https://www.google.com/search?q={query}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Vérifie si Google a bloqué la requête
        if "Our systems have detected unusual traffic" in response.text or "detected unusual traffic" in response.text:
            raise Exception("⚠️ Requête bloquée par Google (Captcha ou anti-bot détecté). Veuillez réessayer plus tard.")

        # Analyse du contenu HTML si tout va bien
        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for result in soup.select(".tF2Cxc"):
            title_tag = result.select_one("h3")
            link_tag = result.select_one("a")

            if title_tag and link_tag:
                results.append({
                    "title": title_tag.text,
                    "link": link_tag["href"]
                })

        return results

    except requests.exceptions.RequestException as req_err:
        raise Exception(f"🌐 Erreur réseau : {req_err}")
    except Exception as err:
        raise Exception(str(err))
        
        
        
def get_startpage_results(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    url = f"https://www.startpage.com/sp/search?query={query}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for result in soup.select("a.result-link"):
            title = result.get_text()
            link = result.get("href")
            if title and link:
                risk = detect_risk(link)
                results.append({
                    "title": title,
                    "link": link,
                    "risk": risk
                })

        return results

    except requests.exceptions.RequestException as req_err:
        raise Exception(f" Erreur réseau : {req_err}")
    except Exception as err:
        raise Exception(f" Erreur : {err}")




def generate_dork(request):
    dork = None
    results = []

    if request.method == 'POST':
        form = DorkForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data.get('keyword')
            domain = form.cleaned_data.get('domain')
            filetype = form.cleaned_data.get('filetype')
            intitle = form.cleaned_data.get('intitle')
            inurl = form.cleaned_data.get('inurl')
            exclude = form.cleaned_data.get('exclude')

            # Construction de la requête
            query_parts = []
            if domain:
                query_parts.append(f"site:{domain}")
            if filetype:
                query_parts.append(f"filetype:{filetype}")
            if intitle:
                query_parts.append(f"intitle:{intitle}")
            if inurl:
                query_parts.append(f"inurl:{inurl}")
            if keyword:
                query_parts.append(keyword)
            if exclude:
                query_parts.append(f"-{exclude}")

            if query_parts:
                query = " ".join(query_parts)

                # Sauvegarde en base
                dork = Dork(
                    keyword=keyword or "",
                    domain=domain or "",
                    query=query,
                    results=""
                )
                dork.save()

                # Recherche Google
                try:
                    results = get_startpage_results(query)

                    dork.results = "\n".join([f"{link} [{risk}]" for link, risk in results])
                    dork.save()
                except Exception as e:
                    print(f"Erreur lors de la récupération des résultats : {e}")

    else:
        form = DorkForm()

    return render(request, 'generate_dork.html', {
        'form': form,
        'dork': dork,
        'results': results
    })



def generate_dork_view(request):
    results = []
    error = None

    if request.method == "POST":
        form = DorkForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            try:
                results = get_google_results(query)
            except Exception as e:
                error = str(e)
    else:
        form = DorkForm()

    return render(request, "generate_dork.html", {
        "form": form,
        "results": results,
        "error": error
    })
