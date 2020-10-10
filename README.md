# L-System Viewer

A viewer for Lindenmayer Systems written in Python / Pygame.

Lots of inspiration is taken from Fractint's L-System implementation.

## L-System
An L-System is defined by three properties:
* An axiom, eg `A`
* A set of replacement rules, eg `(A -> AB), (B -> A)`
* An angle, eg `4`

The angle is defined by an integer number of turns that make up 360
degrees, for example:
* `3` is equivalent to 120 degrees per turn
* `4` is equivalent to 90 degrees per turn
* `36` is equivalent to 10 degrees per turn

Equivalently, the angle in degrees per turn is `360 / angle`

## Graphics State
The graphics state at any point during the drawing process is defined
as follows:
* `x`, the x position of the turtle
* `y`, the y position of the turtle
* `theta`, an angle in degrees
* `phi`, an angle in degrees
* `length`, the drawing length, in arbitrary units
* `reverse`, true if an odd number of `!` command have been encountered
* `colour`, an index into a colour palette

## Drawing Commands

* `F`: Draw forward using angle `theta`
* `G`: Move forward using angle `theta`
* `D`: Draw forward using angle `phi`
* `M`: Move forward using angle `phi`
* `-`: Turn left by `360/angle` (subtract `360/angle` from `theta`)
* `+`: Turn right by `360/angle` (add `360/angle` to `theta`)
* `[`: Save the current graphics state to the graphics stack
* `]`: Restore the topmost graphics state from the graphics stack
* `!`: Reverse the meaning of `+` and `-`, and `\` and `/`
* `|`: Turn 180 degrees (or as close as possible if `angle` is odd)
* `\{NUM}`: Turn left `{NUM}` degrees relative to `phi`
* `/{NUM}`: Turn right `{NUM}` degrees relative to `phi`
* `<{NUM}`: Decrement the current colour index by `{NUM}`
* `>{NUM}`: Increment the current colour index by `{NUM}`
* `C{NUM}`: Set the current colour index to `{NUM}`
* `@{NUM}`: Scale `length` by a factor of `{NUM}` 

Where `{NUM}` is a positive number in decimal, optionally preceded by
`q` and/or `i`, which represent the square root and inverse
(respectively) of the decimal number.

The decimal place may be omitted in the case of integers.
In the case where the decimal place is included, leading or
trailing digits may be omitted if they are zero, ie `.5` and `0.5` are
equivalent, and `5.0`, `5.` and `5` are all equivalent.

* `q2` evaluates to approx `1.414`, ie sqrt(2)
* `i2` evaluates to `0.5`, ie 1/2
* `iq2` evaluates to approx `0.707`, ie 1/sqrt(2)
  * This is equivalent to `qi2`, since 1/sqrt(n) === sqrt(1/n)