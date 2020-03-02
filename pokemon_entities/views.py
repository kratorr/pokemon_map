import folium
import json

from django.http import HttpResponseNotFound, HttpRequest
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()

    pokemon_entities = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, 
            pokemon_entity.lat, 
            pokemon_entity.lon, 
            pokemon_entity.pokemon.title, 
            request.build_absolute_uri(pokemon_entity.pokemon.image.url) if pokemon_entity.pokemon.image else DEFAULT_IMAGE_URL
        )

    pokemons_on_page = []

    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    requested_pokemon_dict = {
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'pokemon_id': requested_pokemon.id,
        'img_url': request.build_absolute_uri(requested_pokemon.image.url)
            if requested_pokemon.image else DEFAULT_IMAGE_URL,
        'description': requested_pokemon.description
    }

    if requested_pokemon.previous_evolution:
        requested_pokemon_dict['previous_evolution'] = {
            'pokemon_id':requested_pokemon.previous_evolution.id,
            'title_ru': requested_pokemon.previous_evolution.title,
            'img_url': request.build_absolute_uri(requested_pokemon.previous_evolution.image.url)
        }
    
    next_evolutions = requested_pokemon.next_evolutions.all()
    
    if next_evolutions:
        next_evolution = next_evolutions[0]
        requested_pokemon_dict['next_evolution'] = {
            'pokemon_id':next_evolution.id,
            'title_ru': next_evolution.title,
            'img_url': request.build_absolute_uri(next_evolution.image.url)
        }



    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entities = requested_pokemon.entities.all()

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_entity.pokemon.title,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url) if pokemon_entity.pokemon.image else DEFAULT_IMAGE_URL
        )

    return render(request, "pokemon.html", context={
            'map': folium_map._repr_html_(),
            'pokemon': requested_pokemon_dict
        }
    )
