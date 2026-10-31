# R21: MCP6002 unused channel

R20 audit shows U1 pins 5, 6, 7 unassigned. For MCP6002 channel B, the proposed stable configuration is pin 5 (non-inverting input) to GND, and pin 6 (inverting input) connected to pin 7 (output), forming a voltage follower. Never short the output to GND. Validate against the actual MCP6002 datasheet and the physical PCB routing before implementing. No PCB was modified by this document.

Other 19 unassigned pads remain; do not connect the battery or fabricate based on DRC alone.
