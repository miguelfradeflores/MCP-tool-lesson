#!/usr/bin/env python3
"""
Pokemon MCP Server - A Model Context Protocol server for Pokemon data
Uses the free PokeAPI (https://pokeapi.co) to fetch Pokemon information
"""

import asyncio
import json
import csv
import os
from typing import Any
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Base URL for the Pokemon API
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"

# Create server instance
server = Server("pokemon-server")


async def fetch_pokemon_data(endpoint: str) -> dict[str, Any]:
    """
    Fetch data from the PokeAPI

    Args:
        endpoint: API endpoint path (e.g., 'pokemon/pikachu')

    Returns:
        JSON response from the API
    """
    url = f"{POKEAPI_BASE_URL}/{endpoint}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        return response.json()


def format_pokemon_info(data: dict[str, Any]) -> str:
    """
    Format Pokemon data into a readable string

    Args:
        data: Raw Pokemon data from the API

    Returns:
        Formatted string with Pokemon information
    """
    name = data.get("name", "Unknown").capitalize()
    pokemon_id = data.get("id", "N/A")
    height = data.get("height", 0) / 10  # Convert to meters
    weight = data.get("weight", 0) / 10  # Convert to kilograms

    # Get types
    types = [t["type"]["name"].capitalize() for t in data.get("types", [])]
    types_str = ", ".join(types)

    # Get abilities
    abilities = [a["ability"]["name"].replace("-", " ").title()
                 for a in data.get("abilities", [])]
    abilities_str = ", ".join(abilities)

    # Get stats
    stats = {s["stat"]["name"]: s["base_stat"] for s in data.get("stats", [])}

    result = f"""
Pokemon: {name} (#{pokemon_id})
Types: {types_str}
Height: {height}m
Weight: {weight}kg
Abilities: {abilities_str}

Base Stats:
  HP: {stats.get('hp', 0)}
  Attack: {stats.get('attack', 0)}
  Defense: {stats.get('defense', 0)}
  Sp. Attack: {stats.get('special-attack', 0)}
  Sp. Defense: {stats.get('special-defense', 0)}
  Speed: {stats.get('speed', 0)}
"""
    return result.strip()


def format_ability_info(data: dict[str, Any]) -> str:
    """
    Format ability data into a readable string

    Args:
        data: Raw ability data from the API

    Returns:
        Formatted string with ability information
    """
    name = data.get("name", "Unknown").replace("-", " ").title()

    # Get English effect entry
    effect_entries = data.get("effect_entries", [])
    effect = "No description available"
    short_effect = ""

    for entry in effect_entries:
        if entry.get("language", {}).get("name") == "en":
            effect = entry.get("effect", effect)
            short_effect = entry.get("short_effect", "")
            break

    result = f"""
Ability: {name}

Short Description: {short_effect}

Full Effect: {effect}
"""
    return result.strip()


def format_type_info(data: dict[str, Any]) -> str:
    """
    Format type data into a readable string

    Args:
        data: Raw type data from the API

    Returns:
        Formatted string with type information
    """
    name = data.get("name", "Unknown").capitalize()

    # Get damage relations
    damage_relations = data.get("damage_relations", {})

    double_damage_to = [t["name"].capitalize()
                        for t in damage_relations.get("double_damage_to", [])]
    half_damage_to = [t["name"].capitalize()
                      for t in damage_relations.get("half_damage_to", [])]
    no_damage_to = [t["name"].capitalize()
                    for t in damage_relations.get("no_damage_to", [])]

    double_damage_from = [t["name"].capitalize()
                          for t in damage_relations.get("double_damage_from", [])]
    half_damage_from = [t["name"].capitalize()
                        for t in damage_relations.get("half_damage_from", [])]
    no_damage_from = [t["name"].capitalize()
                      for t in damage_relations.get("no_damage_from", [])]

    result = f"""
Type: {name}

Attack Effectiveness:
  Super effective against: {", ".join(double_damage_to) if double_damage_to else "None"}
  Not very effective against: {", ".join(half_damage_to) if half_damage_to else "None"}
  No effect against: {", ".join(no_damage_to) if no_damage_to else "None"}

Defense:
  Weak to: {", ".join(double_damage_from) if double_damage_from else "None"}
  Resistant to: {", ".join(half_damage_from) if half_damage_from else "None"}
  Immune to: {", ".join(no_damage_from) if no_damage_from else "None"}
"""
    return result.strip()


@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available tools for the MCP server
    """
    return [
        Tool(
            name="get_pokemon",
            description="Get detailed information about a Pokemon by name or ID. "
                       "Returns stats, types, abilities, height, and weight.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name_or_id": {
                        "type": "string",
                        "description": "Pokemon name (e.g., 'pikachu') or ID number (e.g., '25')"
                    }
                },
                "required": ["name_or_id"]
            }
        ),
        Tool(
            name="get_ability",
            description="Get information about a Pokemon ability by name. "
                       "Returns the effect and description of the ability.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ability_name": {
                        "type": "string",
                        "description": "Name of the ability (e.g., 'static', 'overgrow')"
                    }
                },
                "required": ["ability_name"]
            }
        ),
        Tool(
            name="get_type",
            description="Get information about a Pokemon type. "
                       "Returns effectiveness, weaknesses, and resistances.",
            inputSchema={
                "type": "object",
                "properties": {
                    "type_name": {
                        "type": "string",
                        "description": "Name of the type (e.g., 'fire', 'water', 'electric')"
                    }
                },
                "required": ["type_name"]
            }
        ),
        Tool(
            name="get_pokemon_species",
            description="Get species information about a Pokemon including evolution chain, "
                       "habitat, and Pokedex entries.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name_or_id": {
                        "type": "string",
                        "description": "Pokemon name or ID"
                    }
                },
                "required": ["name_or_id"]
            }
        ),
        Tool(
            name="export_pokemon_to_csv",
            description="Export Pokemon data to a CSV file. Can export one or multiple Pokemon "
                       "with fields including ID, name, types, height, weight, generation, habitat, and legendary status.",
            inputSchema={
                "type": "object",
                "properties": {
                    "pokemon_list": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of Pokemon names or IDs to export (e.g., ['pikachu', 'charizard', '25'])"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Output CSV filename (e.g., 'pokemon_data.csv')",
                        "default": "pokemon_export.csv"
                    }
                },
                "required": ["pokemon_list"]
            }
        )
    ]


async def gather_pokemon_data_for_csv(name_or_id: str) -> dict[str, Any]:
    """
    Gather all Pokemon data needed for CSV export

    Args:
        name_or_id: Pokemon name or ID

    Returns:
        Dictionary with all required fields for CSV export
    """
    # Fetch both pokemon and species data
    pokemon_data = await fetch_pokemon_data(f"pokemon/{name_or_id}")
    species_data = await fetch_pokemon_data(f"pokemon-species/{name_or_id}")

    # Extract basic info
    pokemon_id = pokemon_data.get("id", "N/A")
    name = pokemon_data.get("name", "Unknown").capitalize()
    types = ", ".join([t["type"]["name"].capitalize() for t in pokemon_data.get("types", [])])
    height = pokemon_data.get("height", 0) / 10  # Convert to meters
    weight = pokemon_data.get("weight", 0) / 10  # Convert to kilograms

    # Extract species info
    generation = species_data.get("generation", {}).get("name", "Unknown").upper()
    habitat = species_data.get("habitat", {})
    habitat_name = habitat.get("name", "Unknown").capitalize() if habitat else "Unknown"
    is_legendary = "Yes" if species_data.get("is_legendary", False) else "No"
    is_mythical = "Yes" if species_data.get("is_mythical", False) else "No"

    return {
        "id": pokemon_id,
        "name": name,
        "types": types,
        "height_m": height,
        "weight_kg": weight,
        "generation": generation,
        "habitat": habitat_name,
        "legendary": is_legendary,
        "mythical": is_mythical
    }


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Handle tool calls from the client
    """
    try:
        if name == "get_pokemon":
            name_or_id = arguments.get("name_or_id", "").lower()
            if not name_or_id:
                return [TextContent(
                    type="text",
                    text="Error: Pokemon name or ID is required"
                )]

            data = await fetch_pokemon_data(f"pokemon/{name_or_id}")
            result = format_pokemon_info(data)
            return [TextContent(type="text", text=result)]

        elif name == "get_ability":
            ability_name = arguments.get("ability_name", "").lower()
            if not ability_name:
                return [TextContent(
                    type="text",
                    text="Error: Ability name is required"
                )]

            data = await fetch_pokemon_data(f"ability/{ability_name}")
            result = format_ability_info(data)
            return [TextContent(type="text", text=result)]

        elif name == "get_type":
            type_name = arguments.get("type_name", "").lower()
            if not type_name:
                return [TextContent(
                    type="text",
                    text="Error: Type name is required"
                )]

            data = await fetch_pokemon_data(f"type/{type_name}")
            result = format_type_info(data)
            return [TextContent(type="text", text=result)]

        elif name == "get_pokemon_species":
            name_or_id = arguments.get("name_or_id", "").lower()
            if not name_or_id:
                return [TextContent(
                    type="text",
                    text="Error: Pokemon name or ID is required"
                )]

            data = await fetch_pokemon_data(f"pokemon-species/{name_or_id}")

            # Format species data
            name = data.get("name", "Unknown").capitalize()

            # Get English flavor text
            flavor_texts = data.get("flavor_text_entries", [])
            pokedex_entry = "No Pokedex entry available"
            for entry in flavor_texts:
                if entry.get("language", {}).get("name") == "en":
                    pokedex_entry = entry.get("flavor_text", "").replace("\n", " ")
                    break

            habitat = data.get("habitat", {})
            habitat_name = habitat.get("name", "Unknown").capitalize() if habitat else "Unknown"

            generation = data.get("generation", {}).get("name", "Unknown").upper()

            is_legendary = data.get("is_legendary", False)
            is_mythical = data.get("is_mythical", False)

            result = f"""
Pokemon Species: {name}
Generation: {generation}
Habitat: {habitat_name}
Legendary: {"Yes" if is_legendary else "No"}
Mythical: {"Yes" if is_mythical else "No"}

Pokedex Entry: {pokedex_entry}
"""
            return [TextContent(type="text", text=result.strip())]

        elif name == "export_pokemon_to_csv":
            pokemon_list = arguments.get("pokemon_list", [])
            filename = arguments.get("filename", "pokemon_export.csv")

            if not pokemon_list:
                return [TextContent(
                    type="text",
                    text="Error: pokemon_list is required and cannot be empty"
                )]

            # Gather data for all Pokemon
            all_pokemon_data = []
            failed_pokemon = []

            for pokemon in pokemon_list:
                try:
                    pokemon_data = await gather_pokemon_data_for_csv(str(pokemon).lower())
                    all_pokemon_data.append(pokemon_data)
                except Exception as e:
                    failed_pokemon.append(f"{pokemon} ({str(e)})")

            if not all_pokemon_data:
                return [TextContent(
                    type="text",
                    text=f"Error: Could not fetch data for any Pokemon. Failed: {', '.join(failed_pokemon)}"
                )]

            # Write to CSV
            fieldnames = ["id", "name", "types", "height_m", "weight_kg", "generation", "habitat", "legendary", "mythical"]

            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(all_pokemon_data)

                success_msg = f"Successfully exported {len(all_pokemon_data)} Pokemon to {filename}"
                if failed_pokemon:
                    success_msg += f"\n\nWarning: Failed to fetch data for: {', '.join(failed_pokemon)}"

                success_msg += f"\n\nFile location: {os.path.abspath(filename)}"
                return [TextContent(type="text", text=success_msg)]

            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"Error writing CSV file: {str(e)}"
                )]

        else:
            return [TextContent(
                type="text",
                text=f"Error: Unknown tool '{name}'"
            )]

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return [TextContent(
                type="text",
                text=f"Error: Resource not found. Please check the name/ID and try again."
            )]
        return [TextContent(
            type="text",
            text=f"Error: HTTP {e.response.status_code} - {str(e)}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def main():
    """
    Main entry point for the MCP server
    """
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
