# Dead-tree book tracker

During a Hackathon in 2015 at Balabit I was involved in a project to overhaul our library. Part of that project was
to make sure that the whereabouts of dead-tree books are tracked properly. This script is a piece of that puzzle: it's
basically a quick'n'dirty frontend that augments the default web UI (aka "content server") of Calibre and allows people
to just enter the location of a book if they borrow it or put it back. It is not authenticated at all -- the system's
built on honesty anyway.

As it is 95% just thin wrappers above other tools and practically zero business logic, there are no tests. Also because
it's just a nasty hack.

## Installation instructions

It must be running on the same machine as Calibre does as it needs to interact with its database through the
"calibredb" command. One must set up two new custom columns for this to work: "location" and "previous_location":
those will be used to track the whereabouts of that book. The easiest way to do that are the following commands:

    calibredb add_custom_column location "Current location" text
    calibredb add_custom_column last_location "Last location" text



