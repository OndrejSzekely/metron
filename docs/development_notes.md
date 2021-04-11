# Development Notes
This document covers best practices for development of Metron. 

## Python Dependencies
Metron uses Poetry as dependency and management tool. Therefore, only Poetry should be used (`poetry add` command), no 
Pip or other ways. Developer should distinguish between dependencies for development and usage by an end user. 
For development purposes, add Python dependencies using `--dev` option (`poetry add --dev`).

## Diagram Drawings
All Metron diagrams are drawn using [diagrams.net](https://www.diagrams.net) tool. Diagram projects are found in 
`docs/diagram_projects`.

## Design

### Colour Palette
The colour palette is given by following colours:
- orange: #F9895C
- blue: #65BCD8
- yellow: #F8D643
- dark grey: #545A5E

### Fonts
As a theme font, [QUANTUM](https://www.behance.net/gallery/63174797/QUANTUM-FREE-FONT?tracking_source=project_owner_other_projects) ([download link](https://www.dafont.com/quantum-4.font)) font is used. 
This font should be used for visually appealing diagrams or headlines.

*Tahoma* is used as a standard font everywhere else.
