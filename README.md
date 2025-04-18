# fabaccess-config-generator
Automatische Generierung von Maschinen, Rollen, Aktoren und Aktor-Verbindungen auf Basis einer Maschinenliste im CSV-Format.

## Funktionsumfang
  - Generierung von Maschinen
  - Generierung von Rollen
  - Generierung von Aktoren
  - Generierung von einfachen Aktoren-Verbindungen
  - Export einer gesonderten Rollenliste (interne ID & Anzeigename der Rolle)
  - Abbildung der Struktur mittels Mermaid-Diagramm

Dokumentation unter [https://elem74.github.io/fabaccess-config-generator-docs/](https://elem74.github.io/fabaccess-config-generator-docs/).


# Changelog

## 2025.4
**Neuerungen**
 - Unterstützung für Initiatoren.
 - Import einer bestehenden `bffh.dhall`.

## 2025.2
**Neuerungen**
  - Option zur Erstellung eines Domänen-Managers (`manager_domain`).
  - Option zur Erstellung eines werkstattweiten Benutzers. (`domain_user`)
  - Kommandozeilen-Parameter, um die CSV-Datei mit der Maschinenliste zu definieren.
  - Der verwende CSV-Delimiter wird automatisch erkannt.
  - Die erzeugte Konfiguration wird in einzelnen dhall-Dateien abgelegt, die beim Start von FabAccess nachgeladen werden. Hierfür muss die `bffh.dhall` einmalig angepasst werden.
    - Die FabAccess-Konfiguration in der `bffh.dhall` wird nicht mehr berührt.
    - Kompatibilität mit dem offiziellen dhall-Parser (Ddie bisherigen Platzhalter zum Aktualisieren der `bffh.dhall` bleiben bei Nutzung des Parsers nicht erhalten).

**Bugfixes**
- Crash bei Verwendung der Einstellung `show_machines` behoben.
- Korrektur der erzeugten dhall-Syntax. Der letzte Eintrag einer Datenstruktur wird nicht mehr mit einem Komma abgeschlossen.

**Sonstiges**
- Die erzeugten DHALL-Dateien werden standardgemäß auch im Unterordner `/output` abgelegt.
- Admin-Berechtigungen wurden vollständig auf Wildcard-Zugriffsschema umgestellt. Zuvor wurden Berechtigungen für einzelne Bereiche vergeben.
- Schönere Darstellung der Statusinformationen, wenn das Python-Modul `rich` installiert ist.

**Änderungen in der settings.ini**
- Neue Einstellung `fa_dhall_directory`.
- Die Einstellung `manager_schichtleitung ` entfällt (wird ersetzt von `manager_domain`).
- Die Einstellung `create_file_roles` entfällt. Eine CSV-Datei mit allen Rollennamen und deren FabAcess-IDs wird jetzt standardgemäß erzeugt.
- Die Einstellung `generate_mermaid` entfällt. Eine Textdatei mit Mermaid-Code für ein Werkstattdiagramm wird jetzt standardgemäß erzeugt.
- Die Einstellungen `fa_update_dhall` und `fa_dhall_file` entfallen.

## 2024.6
**Diagrammerzeugung**
- Das Diagramm enthält jetzt eine Icon-Legende.
- Unterschiedliche Icons für Administrator und Manager, um die Unterscheidung zu erleichtern.