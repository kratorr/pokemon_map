import folium
import json

from django.http import HttpResponseNotFound, HttpRequest
from django.shortcuts import render

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
    #with open("pokemon_entities/pokemons.json", encoding="utf-8") as database:
    #    pokemons = json.load(database)['pokemons']
    pokemon_entities = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    
    for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map, 
                pokemon_entity.lat, 
                pokemon_entity.lon, 
                pokemon_entity.pokemon.title, 
                request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            )

    pokemons_on_page = []

    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    #with open("pokemon_entities/pokemons.json", encoding="utf-8") as database:
    #    pokemons = json.load(database)['pokemons']
    requested_pokemon = PokemonEntity.objects.get(id=pokemon_id)
    
    #for pokemon in pokemon_entities:
    #    if pokemon.id == int(pokemon_id):
    #        requested_pokemon = pokemon
    #        break
    #else:
    #    return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    add_pokemon(
            folium_map,
            requested_pokemon.lat,
            requested_pokemon.lon,
            requested_pokemon.pokemon.title,
            request.build_absolute_uri(requested_pokemon.pokemon.image.url)
        )

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': requested_pokemon})


'''
что в JSON-файле.
В словаре должны быть поля img_url, title_ru и т.д., как в JSON-файле.
'''