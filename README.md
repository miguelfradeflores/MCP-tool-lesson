# Pokemon MCP Server

A Model Context Protocol (MCP) server that provides access to Pokemon data from the free [PokeAPI](https://pokeapi.co). This server allows AI assistants and other MCP clients to fetch detailed information about Pokemon, their abilities, types, and species.

## Features

- **Get Pokemon Information**: Fetch detailed stats, types, abilities, height, and weight for any Pokemon
- **Get Ability Details**: Look up information about Pokemon abilities and their effects
- **Get Type Information**: Retrieve type effectiveness, weaknesses, and resistances
- **Get Species Data**: Access species information including Pokedex entries, habitat, and generation

## Installation

1. Install Python 3.10 or higher

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

Run the server directly:

```bash
python pokemon_mcp_server.py
```

### Configuring with Claude Code

To use this MCP server with Claude Code, add it to your MCP settings configuration:

**For MacOS/Linux**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**For Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pokemon": {
      "command": "python",
      "args": ["/absolute/path/to/pokemon_mcp_server.py"]
    }
  }
}
```

After updating the configuration, restart Claude Code.

## Available Tools

### 1. get_pokemon

Get detailed information about a Pokemon by name or ID.

**Parameters:**
- `name_or_id` (string): Pokemon name (e.g., "pikachu") or ID number (e.g., "25")

**Example:**
```
Get information about Pikachu
```

**Response includes:**
- Name and ID
- Types
- Height and weight
- Abilities
- Base stats (HP, Attack, Defense, etc.)

### 2. get_ability

Get information about a Pokemon ability.

**Parameters:**
- `ability_name` (string): Name of the ability (e.g., "static", "overgrow")

**Example:**
```
What does the ability "intimidate" do?
```

**Response includes:**
- Ability name
- Short description
- Full effect details

### 3. get_type

Get information about a Pokemon type.

**Parameters:**
- `type_name` (string): Name of the type (e.g., "fire", "water", "electric")

**Example:**
```
Tell me about the Electric type
```

**Response includes:**
- Type effectiveness (super effective, not very effective, no effect)
- Type weaknesses
- Type resistances and immunities

### 4. get_pokemon_species

Get species information about a Pokemon.

**Parameters:**
- `name_or_id` (string): Pokemon name or ID

**Example:**
```
Get species information for Mewtwo
```

**Response includes:**
- Species name
- Generation
- Habitat
- Legendary/Mythical status
- Pokedex entry

## Example Queries

Once configured with Claude Code, you can ask questions like:

- "What are Charizard's base stats?"
- "Tell me about the Dragon type effectiveness"
- "What does the ability Levitate do?"
- "Is Articuno a legendary Pokemon?"
- "Compare Bulbasaur and Squirtle's stats"

## API Reference

This server uses the [PokeAPI v2](https://pokeapi.co/docs/v2), a free and open Pokemon API. No authentication is required.

## Error Handling

The server includes comprehensive error handling for:
- Invalid Pokemon names or IDs
- Network errors
- API rate limits
- Invalid ability or type names

## Development

### Project Structure

```
.
├── pokemon_mcp_server.py     # Main MCP server implementation
├── test_pokemon_server.py    # Unit tests
├── example_usage.py          # Example usage demonstrations
├── interactive_test.py       # Interactive testing tool
├── run_tests.sh             # Test runner script
├── pytest.ini               # Pytest configuration
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

### Testing

The project includes comprehensive testing tools to verify functionality and demonstrate usage.

#### 1. Unit Tests (pytest)

Run automated unit tests to verify API functionality:

```bash
# Run all tests
pytest test_pokemon_server.py -v

# Run specific test class
pytest test_pokemon_server.py::TestPokemonAPI -v

# Run with coverage
pytest test_pokemon_server.py --cov=pokemon_mcp_server
```

The unit tests cover:
- Fetching Pokemon data by name and ID
- Retrieving ability information
- Getting type effectiveness data
- Accessing species information
- Error handling for invalid requests
- Data formatting functions

#### 2. Example Usage Script

Run a comprehensive demo showing all tools in action:

```bash
python example_usage.py
```

This script demonstrates:
- Getting Pokemon information (Pikachu, Charizard, Mewtwo)
- Fetching ability details (Static, Overgrow, Intimidate, Levitate)
- Retrieving type information (Electric, Fire, Water, Dragon)
- Accessing species data (including legendary Pokemon)
- Error handling examples
- Comparing multiple Pokemon

#### 3. Interactive Testing

Launch an interactive menu to manually test any tool:

```bash
python interactive_test.py
```

Features:
- Interactive menu-driven interface
- Test any tool with custom input
- Quick demo mode with pre-selected Pokemon
- Real-time results display
- Examples and suggestions for inputs

#### 4. Test Runner Script

Use the convenient shell script to access all testing options:

```bash
./run_tests.sh
```

Menu options:
1. Run unit tests (pytest)
2. Run example usage demo
3. Run interactive test
4. Run all automated tests
5. Exit

#### Running Individual Tests

Test specific functionality directly:

```bash
# Test a specific Pokemon
python -c "import asyncio; from pokemon_mcp_server import call_tool; asyncio.run(call_tool('get_pokemon', {'name_or_id': 'pikachu'}))"

# Test an ability
python -c "import asyncio; from pokemon_mcp_server import call_tool; asyncio.run(call_tool('get_ability', {'ability_name': 'static'}))"
```

## License

This project uses data from PokeAPI, which is free and open. Pokemon and Pokemon character names are trademarks of Nintendo.

## Contributing

Feel free to submit issues or pull requests to enhance the functionality of this MCP server.

## Resources

- [PokeAPI Documentation](https://pokeapi.co/docs/v2)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
