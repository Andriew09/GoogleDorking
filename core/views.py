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
        risk_level = "⚠️ Fichier exposé"
    if any(rk in link.lower() for rk in risk_keywords):
        risk_level = "⛔ Risque élevé"
    return risk_level


def get_google_results(query):
    time.sleep(random.uniform(1.5, 3))  # Anti-bot

    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    for g in soup.find_all('div', class_='tF2Cxc'):
        link_tag = g.find('a')
        if link_tag and link_tag['href']:
            href = link_tag['href']
            risk = detect_risk(href)
            links.append((href, risk))

    return links


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
                    results = get_google_results(query)
                    # Stockage brut en texte dans le champ results si besoin
                    dork.results = "\n".join([f"{link} [{risk}]" for link, risk in results])
                    dork.save()
                except Exception as e:
                    results = []

    else:
        form = DorkForm()

    return render(request, 'generate_dork.html', {
        'form': form,
        'dork': dork,
        'results': results
    })


def export_dorks_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dorks.csv"'

    writer = csv.writer(response)
    writer.writerow(['Keyword', 'Domain', 'Query', 'Results'])

    for dork in Dork.objects.all():
        writer.writerow([dork.keyword, dork.domain, dork.query, dork.results])

    return response
    

def export_dorks_json(request):
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="dorks.json"'

    dorks = list(Dork.objects.values('keyword', 'domain', 'query', 'results'))
    response.write(json.dumps(dorks, indent=4))

    return response
    
