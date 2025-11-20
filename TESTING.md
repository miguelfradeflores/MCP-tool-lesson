# Testing Guide - Pokemon MCP Server

Quick reference guide for testing the Pokemon MCP Server.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
./run_tests.sh
```

## Test Files Overview

| File | Purpose | Usage |
|------|---------|-------|
| `test_pokemon_server.py` | Unit tests with pytest | `pytest test_pokemon_server.py -v` |
| `example_usage.py` | Automated demo of all tools | `python example_usage.py` |
| `interactive_test.py` | Manual interactive testing | `python interactive_test.py` |
| `run_tests.sh` | Unified test runner menu | `./run_tests.sh` |

## Testing Methods

### 1. Automated Unit Tests

```bash
# Run all tests
pytest test_pokemon_server.py -v

# Run specific test class
pytest test_pokemon_server.py::TestPokemonAPI -v

# Run specific test
pytest test_pokemon_server.py::TestPokemonAPI::test_fetch_pokemon_pikachu -v

# Show test output
pytest test_pokemon_server.py -v -s

# Run with coverage (requires pytest-cov)
pytest test_pokemon_server.py --cov=pokemon_mcp_server --cov-report=html
```

### 2. Example Usage Demo

```bash
# Run full demonstration
python example_usage.py

# The script will automatically:
# - Test get_pokemon with multiple Pokemon
# - Test get_ability with various abilities
# - Test get_type for different types
# - Test get_pokemon_species
# - Demonstrate error handling
# - Compare Pokemon stats
```

### 3. Interactive Testing

```bash
# Launch interactive menu
python interactive_test.py

# Options available:
# 1. Get Pokemon Information (enter any Pokemon name/ID)
# 2. Get Ability Information (enter any ability)
# 3. Get Type Information (enter any type)
# 4. Get Species Information (enter any Pokemon)
# 5. Run Quick Demo (pre-configured examples)
# 6. Exit
```

### 4. Test Runner Menu

```bash
# Run the test runner
./run_tests.sh

# Choose from menu:
# 1. Run unit tests (pytest)
# 2. Run example usage demo
# 3. Run interactive test
# 4. Run all automated tests
# 5. Exit
```

## Test Data Examples

### Pokemon Names/IDs to Test
- **Popular**: pikachu, charizard, mewtwo, dragonite, eevee
- **By ID**: 1 (bulbasaur), 25 (pikachu), 150 (mewtwo)
- **Starters**: bulbasaur, charmander, squirtle
- **Legendary**: mewtwo, articuno, zapdos, moltres, lugia, ho-oh

### Abilities to Test
- static, overgrow, blaze, torrent
- levitate, intimidate, swift-swim
- pressure, trace, synchronize

### Types to Test
- **Common**: normal, fire, water, electric, grass
- **Special**: dragon, psychic, dark, steel, fairy
- **All 18 types**: normal, fighting, flying, poison, ground, rock, bug, ghost, steel, fire, water, grass, electric, psychic, ice, dragon, dark, fairy

## Expected Results

### get_pokemon
```
Pokemon: Pikachu (#25)
Types: Electric
Height: 0.4m
Weight: 6.0kg
Abilities: Static, Lightning Rod

Base Stats:
  HP: 35
  Attack: 55
  Defense: 40
  ...
```

### get_ability
```
Ability: Static

Short Description: Has a 30% chance to paralyze attacking Pokémon on contact.

Full Effect: ...
```

### get_type
```
Type: Electric

Attack Effectiveness:
  Super effective against: Water, Flying
  Not very effective against: Electric, Grass, Dragon
  ...
```

### get_pokemon_species
```
Pokemon Species: Mewtwo
Generation: GENERATION-I
Habitat: Rare
Legendary: Yes
Mythical: No

Pokedex Entry: ...
```

## Error Testing

Test error handling with:

```bash
# Invalid Pokemon name
python -c "import asyncio; from pokemon_mcp_server import call_tool; print(asyncio.run(call_tool('get_pokemon', {'name_or_id': 'fakemon'})))"

# Invalid ability
python -c "import asyncio; from pokemon_mcp_server import call_tool; print(asyncio.run(call_tool('get_ability', {'ability_name': 'notreal'})))"

# Missing parameters
python -c "import asyncio; from pokemon_mcp_server import call_tool; print(asyncio.run(call_tool('get_pokemon', {})))"
```

Expected error messages:
- `Error: Resource not found. Please check the name/ID and try again.`
- `Error: Pokemon name or ID is required`

## Quick Commands

```bash
# One-liner tests
python -c "import asyncio; from pokemon_mcp_server import call_tool; result = asyncio.run(call_tool('get_pokemon', {'name_or_id': 'pikachu'})); print(result[0].text)"

python -c "import asyncio; from pokemon_mcp_server import call_tool; result = asyncio.run(call_tool('get_type', {'type_name': 'fire'})); print(result[0].text)"

python -c "import asyncio; from pokemon_mcp_server import call_tool; result = asyncio.run(call_tool('get_ability', {'ability_name': 'levitate'})); print(result[0].text)"
```

## Continuous Integration

For CI/CD pipelines:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests with exit code
pytest test_pokemon_server.py -v --tb=short

# Generate coverage report
pytest test_pokemon_server.py --cov=pokemon_mcp_server --cov-report=term-missing

# Run example (should not fail)
python example_usage.py
```

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure you're in the correct directory
   ```bash
   cd /path/to/mcp_tests
   ```

2. **Module Not Found**: Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. **Network Error**: Check internet connection (PokeAPI requires internet)

4. **API Rate Limit**: Wait a few moments between requests

5. **Permission Denied** on run_tests.sh:
   ```bash
   chmod +x run_tests.sh
   ```

## Performance Testing

Test API response times:

```python
import asyncio
import time
from pokemon_mcp_server import call_tool

async def benchmark():
    start = time.time()
    await call_tool("get_pokemon", {"name_or_id": "pikachu"})
    end = time.time()
    print(f"Time: {end - start:.2f}s")

asyncio.run(benchmark())
```

## Best Practices

1. Always run unit tests before committing changes
2. Test with both Pokemon names and IDs
3. Verify error handling works correctly
4. Test edge cases (e.g., Pokemon #1, legendary Pokemon)
5. Check API responses match expected format

## Additional Resources

- [PokeAPI Documentation](https://pokeapi.co/docs/v2)
- [Pytest Documentation](https://docs.pytest.org/)
- [Python asyncio Guide](https://docs.python.org/3/library/asyncio.html)
