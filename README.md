# Dead-tree book tracker

During a Hackathon in 2015 at Balabit I was involved in a project to overhaul our library. Part of that project was
to make sure that the whereabouts of dead-tree books are tracked properly. This script is a piece of that puzzle: it's
basically a quick'n'dirty frontend that augments the default web UI (aka "content server") of Calibre and allows people
to just enter the location of a book if they borrow it or put it back. It is not authenticated at all -- the system's
built on honesty anyway.

As it is 95% just thin wrappers above other tools and practically zero business logic, there are no tests. Also because
it's just a nasty hack.

## Installation instructions

### Basics

It must be running on the same machine as Calibre does as it needs to interact with its database through the
"calibredb" command. One must set up two new custom columns for this to work: "location" and "previous_location":
those will be used to track the whereabouts of that book. The easiest way to do that are the following commands:

    calibredb add_custom_column location "Current location" text
    calibredb add_custom_column last_location "Last location" text

Make sure you copy `configuration.py.sample` to `configuration.py` and specify the root URL for Calibre.

### Augmenting the Calibre Content Server web UI

The values of the custom fields ("Current location" and "Last location") appear automatically on the Calibre UI,
you don't need to do anything to change that. But it'd be great to have a link on that UI this tool so that the
user can immediately change the location of a book.

Calibre allows the customization of the UI of the content server but it's a bit tricky. The process is described
in the [Calibre manual](http://manual.calibre-ebook.com/customize.html#overriding-icons-templates-et-cetera). What
you need to do is the following:

1. Find the location of the default templates for the content server. If installed from package on an Ubuntu, for
example, they're at `/usr/share/calibre/content_server/`
2. Find out where's your configuration directory for Calibre located. The easiest way to do that is to go to 
Preferences->Advanced->Miscellaneous in Calibre and click Open calibre configuration directory that will bring you there.
On a default Ubuntu install, it's at `~/.config/calibre`
3. Create a directory called `resources` in that config directory
4. Copy the entire default `content_sever` directory here
5. Overwrite the `browse/summary.html` with the version in this repository.
6. Edit the following line in `summary.html` to make sure it contains the right URL for this tool instead of `127.0.0.1`
```html
<a href="http://127.0.0.1:5000/{id}/" title="Update location">Location</a>
```
7. Restart the content server for the changes to take effect.

