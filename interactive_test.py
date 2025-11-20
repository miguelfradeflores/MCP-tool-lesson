#!/usr/bin/env python3
"""
Interactive test script for the Pokemon MCP Server
Allows manual testing of all tools with user input
"""

import asyncio
from pokemon_mcp_server import call_tool


async def interactive_menu():
    """Display interactive menu and handle user choices"""

    while True:
        print("\n" + "="*60)
        print("POKEMON MCP SERVER - INTERACTIVE TEST")
        print("="*60)
        print("\nAvailable Tools:")
        print("1. Get Pokemon Information")
        print("2. Get Ability Information")
        print("3. Get Type Information")
        print("4. Get Species Information")
        print("5. Run Quick Demo")
        print("6. Exit")
        print("="*60)

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            await test_get_pokemon_interactive()
        elif choice == "2":
            await test_get_ability_interactive()
        elif choice == "3":
            await test_get_type_interactive()
        elif choice == "4":
            await test_get_species_interactive()
        elif choice == "5":
            await run_quick_demo()
        elif choice == "6":
            print("\nGoodbye! Thanks for testing the Pokemon MCP Server.")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")


async def test_get_pokemon_interactive():
    """Interactive test for get_pokemon tool"""
    print("\n" + "-"*60)
    print("GET POKEMON INFORMATION")
    print("-"*60)
    print("Enter a Pokemon name (e.g., 'pikachu') or ID (e.g., '25')")
    print("Popular examples: pikachu, charizard, mewtwo, bulbasaur, dragonite")

    name_or_id = input("\nPokemon name or ID: ").strip().lower()

    if not name_or_id:
        print("Error: No input provided.")
        return

    print("\nFetching Pokemon data...")
    try:
        result = await call_tool("get_pokemon", {"name_or_id": name_or_id})
        print("\n" + result[0].text)
    except Exception as e:
        print(f"\nError: {e}")


async def test_get_ability_interactive():
    """Interactive test for get_ability tool"""
    print("\n" + "-"*60)
    print("GET ABILITY INFORMATION")
    print("-"*60)
    print("Enter an ability name (e.g., 'static', 'overgrow')")
    print("Popular examples: static, overgrow, levitate, intimidate, blaze")

    ability_name = input("\nAbility name: ").strip().lower()

    if not ability_name:
        print("Error: No input provided.")
        return

    print("\nFetching ability data...")
    try:
        result = await call_tool("get_ability", {"ability_name": ability_name})
        print("\n" + result[0].text)
    except Exception as e:
        print(f"\nError: {e}")


async def test_get_type_interactive():
    """Interactive test for get_type tool"""
    print("\n" + "-"*60)
    print("GET TYPE INFORMATION")
    print("-"*60)
    print("Enter a Pokemon type (e.g., 'fire', 'water')")
    print("Available types: normal, fire, water, electric, grass, ice, fighting,")
    print("                 poison, ground, flying, psychic, bug, rock, ghost,")
    print("                 dragon, dark, steel, fairy")

    type_name = input("\nType name: ").strip().lower()

    if not type_name:
        print("Error: No input provided.")
        return

    print("\nFetching type data...")
    try:
        result = await call_tool("get_type", {"type_name": type_name})
        print("\n" + result[0].text)
    except Exception as e:
        print(f"\nError: {e}")


async def test_get_species_interactive():
    """Interactive test for get_pokemon_species tool"""
    print("\n" + "-"*60)
    print("GET SPECIES INFORMATION")
    print("-"*60)
    print("Enter a Pokemon name or ID")
    print("Try legendary Pokemon: mewtwo, articuno, zapdos, moltres, lugia")

    name_or_id = input("\nPokemon name or ID: ").strip().lower()

    if not name_or_id:
        print("Error: No input provided.")
        return

    print("\nFetching species data...")
    try:
        result = await call_tool("get_pokemon_species", {"name_or_id": name_or_id})
        print("\n" + result[0].text)
    except Exception as e:
        print(f"\nError: {e}")


async def run_quick_demo():
    """Run a quick demo with predefined Pokemon"""
    print("\n" + "-"*60)
    print("QUICK DEMO")
    print("-"*60)

    demos = [
        ("Pokemon: Pikachu", "get_pokemon", {"name_or_id": "pikachu"}),
        ("Ability: Levitate", "get_ability", {"ability_name": "levitate"}),
        ("Type: Dragon", "get_type", {"type_name": "dragon"}),
        ("Species: Mewtwo", "get_pokemon_species", {"name_or_id": "mewtwo"}),
    ]

    for title, tool_name, arguments in demos:
        print(f"\n{'='*60}")
        print(f"Demo: {title}")
        print('='*60)

        try:
            result = await call_tool(tool_name, arguments)
            print(result[0].text)
        except Exception as e:
            print(f"Error: {e}")

        input("\nPress Enter to continue...")


async def main():
    """Main entry point"""
    print("\nWelcome to the Pokemon MCP Server Interactive Test!")
    print("This tool allows you to test all available MCP tools.")

    try:
        await interactive_menu()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
