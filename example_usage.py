#!/usr/bin/env python3
"""
Example usage script for testing the Pokemon MCP Server tools
This script demonstrates how to use each tool in the server
"""

import asyncio
from pokemon_mcp_server import call_tool


async def test_get_pokemon():
    """Test the get_pokemon tool"""
    print("\n" + "="*60)
    print("Testing: get_pokemon tool")
    print("="*60)

    # Test with Pokemon name
    print("\n1. Getting Scizor by name:")
    result = await call_tool("get_pokemon", {"name_or_id": "scizor"})
    print(result[0].text)

    # Test with Pokemon ID
    print("\n2. Getting Charizard by ID (6):")
    result = await call_tool("get_pokemon", {"name_or_id": "6"})
    print(result[0].text)

    # Test with another popular Pokemon
    print("\n3. Getting Mewtwo:")
    result = await call_tool("get_pokemon", {"name_or_id": "mewtwo"})
    print(result[0].text)


async def test_get_ability():
    """Test the get_ability tool"""
    print("\n" + "="*60)
    print("Testing: get_ability tool")
    print("="*60)

    abilities = ["static", "overgrow", "intimidate", "levitate"]

    for ability in abilities:
        print(f"\n{abilities.index(ability) + 1}. Getting ability: {ability}")
        result = await call_tool("get_ability", {"ability_name": ability})
        print(result[0].text)


async def test_get_type():
    """Test the get_type tool"""
    print("\n" + "="*60)
    print("Testing: get_type tool")
    print("="*60)

    types = ["psychic", "fire", "ice", "dragon"]

    for poke_type in types:
        print(f"\n{types.index(poke_type) + 1}. Getting type: {poke_type}")
        result = await call_tool("get_type", {"type_name": poke_type})
        print(result[0].text)


async def test_get_pokemon_species():
    """Test the get_pokemon_species tool"""
    print("\n" + "="*60)
    print("Testing: get_pokemon_species tool")
    print("="*60)

    species = ["pikachu", "mewtwo", "articuno", "bulbasaur"]

    for species_name in species:
        print(f"\n{species.index(species_name) + 1}. Getting species: {species_name}")
        result = await call_tool("get_pokemon_species", {"name_or_id": species_name})
        print(result[0].text)


async def test_error_handling():
    """Test error handling"""
    print("\n" + "="*60)
    print("Testing: Error Handling")
    print("="*60)

    # Test invalid Pokemon
    print("\n1. Testing invalid Pokemon name:")
    result = await call_tool("get_pokemon", {"name_or_id": "invalidpokemon123"})
    print(result[0].text)

    # Test invalid ability
    print("\n2. Testing invalid ability:")
    result = await call_tool("get_ability", {"ability_name": "notanability"})
    print(result[0].text)

    # Test missing parameter
    print("\n3. Testing missing parameter:")
    result = await call_tool("get_pokemon", {})
    print(result[0].text)


async def test_comparison():
    """Test comparing multiple Pokemon"""
    print("\n" + "="*60)
    print("Testing: Pokemon Comparison")
    print("="*60)

    starters = ["bulbasaur", "charmander", "squirtle"]

    print("\nComparing original starter Pokemon:")
    for starter in starters:
        result = await call_tool("get_pokemon", {"name_or_id": starter})
        print(result[0].text)
        print("-" * 60)


async def main():
    """Run all example tests"""
    print("\n" + "="*60)
    print("POKEMON MCP SERVER - EXAMPLE USAGE")
    print("="*60)

    tests = [
        ("Pokemon Information", test_get_pokemon),
        ("Abilities", test_get_ability),
        ("Types", test_get_type),
        ("Species Information", test_get_pokemon_species),
        ("Error Handling", test_error_handling),
        ("Pokemon Comparison", test_comparison),
    ]

    for test_name, test_func in tests:
        try:
            await test_func()
        except Exception as e:
            print(f"\nError in {test_name}: {e}")

    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
