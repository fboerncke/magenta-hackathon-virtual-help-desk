# Virtual Help Desk Skill for Hello Magenta Assistant

This repository contains the code related deliverables for the Remote Rhapsody Online Hackathon.


## YouTube Video

The YouTube video describing a typical usage scenario can be found here: "tbd"

## Code Artifacts

What you will find in the folders:

### hackathon-conf

Definitions for launch phrase and parameters using regular expressions.

### Folder: "images"

Image artifacts used for the presentation.

### Folder: "serverless"

Backend logic for the service which is used from the python code. The lambda function build in JavaScript makes requests to the Voice CMS db and triggers writing new entries in case some keyword was not yet supported.

### Folder: "skill-catalog"

Catalog file for the Hello Magenta App entry.

### Folder: "skill-helpdesk-python"

The skill implementation itself. The file "impl/helpdesk.py" contains the business logic of the skill.

## The Issue

![The issue](https://github.com/fboerncke/magenta-hackathon-virtual-help-desk/blob/main/images/theIssue.png "The issue")

## Architecture

![The issue](https://github.com/fboerncke/magenta-hackathon-virtual-help-desk/blob/main/images/theSolution.png "The issue")
