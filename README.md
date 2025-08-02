# Epson Printer Integration for Home Assistant

<p align="center">
  <img src="https://global.epson.com/assets/img/logo.svg" width="200" alt="Epson Logo">
</p>

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]][license]
[![hacs][hacsbadge]][hacs]

A Home Assistant custom integration for Epson Network Printers that allows you to monitor ink levels and printer status directly from Home Assistant.

## Features

- 🖨️ Real-time ink level monitoring for all colors
- 🎨 Individual sensors for Black, Magenta, Cyan, Yellow ink
- 🧽 Cleaning cartridge level monitoring
- 📊 Percentage-based level display
- ⚙️ Configurable update interval (default: 1 hour)
- 🏠 Easy configuration through Home Assistant UI
- 🎯 Professional Epson branding in interface
- 📱 Mobile-friendly Lovelace cards included
- 🔔 Automation support for low ink notifications

## Supported Devices

- Epson network printers with ink level reporting capability
- Tested with various Epson inkjet printer models
- Requires network connectivity (IP address access)

## Installation

### HACS (Recommended)

1. Make sure you have [HACS](https://hacs.xyz/) installed in your Home Assistant
2. In HACS, go to "Integrations"
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add this repository URL: `https://github.com/maciejwaloszczyk/homeassistant-epson-printer`
5. Select "Integration" as the category
6. Click "Add"
7. Search for "Epson Printer Monitor" in HACS
8. Click "Download"
9. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/maciejwaloszczyk/homeassistant-epson-printer/releases)
2. Extract the zip file
3. Copy the `custom_components/epson_printer` folder to your Home Assistant `custom_components` directory
4. Restart Home Assistant

### Dependencies

Make sure the `epsonprinter` Python package is installed in your Home Assistant environment:

```bash
pip install epsonprinter
```

## Configuration

### UI Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for **Epson Printer Monitor**
4. Enter your printer configuration:
   - **Printer IP Address**: The IP address of your Epson printer (e.g., `192.168.0.5`)
   - **Update Interval**: How often to check ink levels in seconds (default: 3600 = 1 hour)
5. Click **Submit**

The integration will automatically create sensors for all available ink cartridges and cleaning cartridge.

## Entities

After configuration, the following sensor entities will be available:

| Entity ID | Name | Unit | Description |
|-----------|------|------|-------------|
| `sensor.epson_printer_black_ink` | Black Ink | % | Black ink level |
| `sensor.epson_printer_magenta_ink` | Magenta Ink | % | Magenta ink level |
| `sensor.epson_printer_cyan_ink` | Cyan Ink | % | Cyan ink level |
| `sensor.epson_printer_yellow_ink` | Yellow Ink | % | Yellow ink level |
| `sensor.epson_printer_cleaning_cartridge` | Cleaning Cartridge | % | Cleaning cartridge level |

## Usage

### Basic Lovelace Card

```yaml
type: entities
title: Epson Printer - Ink Levels
entities:
  - entity: sensor.epson_printer_black_ink
    name: Black
  - entity: sensor.epson_printer_magenta_ink  
    name: Magenta
  - entity: sensor.epson_printer_cyan_ink
    name: Cyan
  - entity: sensor.epson_printer_yellow_ink
    name: Yellow
  - entity: sensor.epson_printer_cleaning_cartridge
    name: Cleaning Cartridge
```

### Gauge Cards

```yaml
type: gauge
entity: sensor.epson_printer_black_ink
name: Black Ink
min: 0
max: 100
severity:
  green: 50
  yellow: 25
  red: 0
```

### Low Ink Automation

```yaml
automation:
  - alias: "Low ink level notification"
    trigger:
      - platform: numeric_state
        entity_id: 
          - sensor.epson_printer_black_ink
          - sensor.epson_printer_magenta_ink
          - sensor.epson_printer_cyan_ink
          - sensor.epson_printer_yellow_ink
        below: 10
    action:
      - service: notify.mobile_app
        data:
          title: "Low ink level"
          message: "{{ trigger.to_state.name }} is {{ trigger.to_state.state }}%"
```

## Testing

Use the included test script to verify printer connectivity before setup:

```bash
python test_printer.py 192.168.0.5
```

This will test the connection and display current ink levels.

## Troubleshooting

### Common Issues

1. **Cannot connect to printer**
   - Verify the printer IP address is correct
   - Ensure the printer is powered on and connected to network
   - Check firewall settings
   - Test connectivity using the test script

2. **Sensors show "unavailable"**
   - Check Home Assistant logs for errors
   - Verify `epsonprinter` package is installed
   - Ensure printer model supports ink level reporting

3. **Some sensors missing**
   - Not all printer models support all ink types
   - Cleaning cartridge may not be available on all models
   - Check printer specifications

### Debug Logging

To enable debug logging, add this to your `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.epson_printer: debug
```

## Requirements

- Home Assistant 2023.1+
- Python 3.10+
- Epson network printer with ink level reporting
- Network connectivity to printer

## Dependencies

- [epsonprinter](https://pypi.org/project/epsonprinter/) - Python library for Epson printer communication

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with your printer
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you find this integration useful, please consider starring the repository!

For issues and feature requests, please use the [GitHub Issues](https://github.com/maciejwaloszczyk/homeassistant-epson-printer/issues) page.

---

[releases-shield]: https://img.shields.io/github/release/maciejwaloszczyk/homeassistant-epson-printer.svg?style=for-the-badge
[releases]: https://github.com/maciejwaloszczyk/homeassistant-epson-printer/releases
[license-shield]: https://img.shields.io/github/license/maciejwaloszczyk/homeassistant-epson-printer.svg?style=for-the-badge
[license]: https://github.com/maciejwaloszczyk/homeassistant-epson-printer/blob/master/LICENSE
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
