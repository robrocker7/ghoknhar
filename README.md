ghoknhar
========

# Introduction

This project is a tinker house for me to develop my home automation software. My planned architecture will be to have this platform as the interaction layer for the ZWave integration.

This project is not meant to be easily replicatable and will include a lot of custom code for my personal use cases.

# Plans

To get the project started without too much personal feature creep I am keeping the first implementation of the project simple and then I will expand the feature set greatly as the technology evolves.

## Step One

Get the basic user authentication system working
Manually add devices and their IDs from the django admin
Be able to push a button on the website and it makes the appropriate api calls

## Step Two

Sync the DB based upon the data recieved from the ZWave configuration api
Write a communication wrapper for communicating with the ZWave api
Local splunk instance to store events

## Step Three

Building Room objects
Build cron style events for automation
Build ITET (if then else then) trees for interacting with NEST and other non-zwave controllers.
