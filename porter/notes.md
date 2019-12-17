# Fugue generator v1

## Chord walking
- Moves towards farther away point for first two measures with high certainty, then reverses to go back

## Melody generation
- Random key
- Notes that chords are on are guaranteed to be in chord
- Notes are randomly generated, but:
	- Pitch is likely to follow similar rise-fall pattern of previous notes (direction, distance)
	- Length of note is likely to be the same as previous note
	- Notes don't extend past measures

## Fugue stuff
- After first bit, chords are shifted down by a fifth
- A second melody is generated on top in the same way, but notes are unlikely to be placed at the same time there is another note in the previous melody

## Future
- More voices
- Velocity control (older voices have lower velocity)
- Faster notes
