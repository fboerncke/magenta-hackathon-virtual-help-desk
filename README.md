# Virtual Help Desk Skill for Hello Magenta Assistant

This repository contains the code related deliverables for the Remote Rhapsody Online Hackathon.


## YouTube Video

The YouTube video describing a typical usage scenario can be found here: [Virtual Help Desk Promo Video - https://youtu.be/RlqjRHNi30k](https://youtu.be/RlqjRHNi30k)

## The Issue

![The issue](https://github.com/fboerncke/magenta-hackathon-virtual-help-desk/blob/main/images/theIssue.png "The issue")

## The Solution

![The issue](https://github.com/fboerncke/magenta-hackathon-virtual-help-desk/blob/main/images/theSolution.png "The issue")

## The Big Picture

![The big picture](https://github.com/fboerncke/magenta-hackathon-virtual-help-desk/blob/main/images/bigPicture.png "The big picture")

## Voice CMS
Using the services from Airtable we built a Voice CMS to maintain the contents of the skill.

Access to the Voice CMS/Airtable is possible via a share link. For reasons of security I cannot share the link in GitHub but only on request.

![Voice CMS](https://github.com/fboerncke/magenta-hackathon-virtual-help-desk/blob/main/images/backendDataAirtable.png "Voice CMS")


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

