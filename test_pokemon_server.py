#!/usr/bin/env python3
"""
Unit tests for the Pokemon MCP Server
"""

import asyncio
import pytest
from pokemon_mcp_server import (
    fetch_pokemon_data,
    format_pokemon_info,
    format_ability_info,
    format_type_info,
)


class TestPokemonAPI:
    """Test Pokemon API data fetching"""

    @pytest.mark.asyncio
    async def test_fetch_pokemon_pikachu(self):
        """Test fetching Pikachu's data"""
        data = await fetch_pokemon_data("pokemon/pikachu")
        assert data is not None
        assert data["name"] == "pikachu"
        assert data["id"] == 25
        assert "types" in data
        assert "abilities" in data

    @pytest.mark.asyncio
    async def test_fetch_pokemon_by_id(self):
        """Test fetching Pokemon by ID"""
        data = await fetch_pokemon_data("pokemon/1")
        assert data is not None
        assert data["name"] == "bulbasaur"
        assert data["id"] == 1

    @pytest.mark.asyncio
    async def test_fetch_ability(self):
        """Test fetching ability data"""
        data = await fetch_pokemon_data("ability/static")
        assert data is not None
        assert data["name"] == "static"
        assert "effect_entries" in data

    @pytest.mark.asyncio
    async def test_fetch_type(self):
        """Test fetching type data"""
        data = await fetch_pokemon_data("type/electric")
        assert data is not None
        assert data["name"] == "electric"
        assert "damage_relations" in data

    @pytest.mark.asyncio
    async def test_fetch_species(self):
        """Test fetching species data"""
        data = await fetch_pokemon_data("pokemon-species/mewtwo")
        assert data is not None
        assert data["name"] == "mewtwo"
        assert data["is_legendary"] is True

    @pytest.mark.asyncio
    async def test_fetch_invalid_pokemon(self):
        """Test fetching invalid Pokemon returns error"""
        with pytest.raises(Exception):
            await fetch_pokemon_data("pokemon/invalidpokemon12345")


class TestFormatting:
    """Test data formatting functions"""

    @pytest.mark.asyncio
    async def test_format_pokemon_info(self):
        """Test Pokemon info formatting"""
        data = await fetch_pokemon_data("pokemon/pikachu")
        result = format_pokemon_info(data)

        assert "Pikachu" in result
        assert "#25" in result
        assert "Electric" in result
        assert "HP:" in result
        assert "Attack:" in result

    @pytest.mark.asyncio
    async def test_format_ability_info(self):
        """Test ability info formatting"""
        data = await fetch_pokemon_data("ability/overgrow")
        result = format_ability_info(data)

        assert "Overgrow" in result
        assert "Effect:" in result or "Description:" in result

    @pytest.mark.asyncio
    async def test_format_type_info(self):
        """Test type info formatting"""
        data = await fetch_pokemon_data("type/fire")
        result = format_type_info(data)

        assert "Fire" in result
        assert "effective" in result.lower()


class TestSpecificPokemon:
    """Test specific Pokemon to verify data accuracy"""

    @pytest.mark.asyncio
    async def test_charizard_stats(self):
        """Test Charizard has correct types"""
        data = await fetch_pokemon_data("pokemon/charizard")
        types = [t["type"]["name"] for t in data["types"]]
        assert "fire" in types
        assert "flying" in types

    @pytest.mark.asyncio
    async def test_legendary_status(self):
        """Test legendary Pokemon detection"""
        # Mewtwo should be legendary
        mewtwo = await fetch_pokemon_data("pokemon-species/mewtwo")
        assert mewtwo["is_legendary"] is True

        # Pikachu should not be legendary
        pikachu = await fetch_pokemon_data("pokemon-species/pikachu")
        assert pikachu["is_legendary"] is False

    @pytest.mark.asyncio
    async def test_type_effectiveness(self):
        """Test type effectiveness relationships"""
        data = await fetch_pokemon_data("type/water")

        # Water should be super effective against Fire
        double_damage_to = [t["name"] for t in data["damage_relations"]["double_damage_to"]]
        assert "fire" in double_damage_to

        # Water should be weak to Electric
        double_damage_from = [t["name"] for t in data["damage_relations"]["double_damage_from"]]
        assert "electric" in double_damage_from


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
