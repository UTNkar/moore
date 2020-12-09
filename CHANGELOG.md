# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [2.6.0] - 2020-12-09

### Changed

- Wagtail from 2.11.1 to 2.11.2
- Rebuilding of header
- Django from 3.1.3 to 3.1.4
- Phonenumbers from 8.12.13 to 8.12.14

## [2.5.0] - 2020-11-16

### Changed

- Role type styrelsen can now see all applications, roles and positions for the role types presidium, group leader, engaged regardless of which teams they belong to
- Updated phonenumbers to 8.12.13

## [2.4.0] - 2020-11-06

### Added

- Added a membercheck as a wagtail block and API

### Changed

- Updated wagtail to 2.11
- Updated django to 3.1.3
- Updated djangorestframework to 3.12.2
- Updated phonenumbers to 8.12.12

## [2.3.0] - 2020-10-24

### Added

- Added editorconfig
- Added api for member check
- Added linebreaks to qualifications when inspecting an application
- Added recaptcha to formpages
- Added a button for switching language

### Changed

- Replaced psycop2-binary with psycopg2
- Updated djangorestframework to 3.12.1
- Updated phonenumbers to 8.12.11
- Updated django to 3.1.2
- Updated wagtail to 2.10.2

## [2.2.0] - 2020-09-04

### Changed

- Rebuilt the counters block
- Updated wagtailmedia to 0.6.0
- Updated phonenumbers to 8.12.9

## [2.1.4] - 2020-08-12

### Fixed

- Fix a bug that caused latest news to use wrong images.
- Fix the instagram block so that it shows pictures again

## [2.1.3] - 2020-08-11

### Changed

- Made manage.py executable

## [2.1.2] - 2020-08-11

### Changed

- Updated requests to 2.24.0
- Updated phonenumbers to 8.12.7
- Updated wagtail to 2.7.4

### Added

- Added support for developing moore with docker

## [2.1.1] - 2020-06-10

### Changed

- Updated phonenumbers to 8.12.5
- Updated django to 2.2.13

## [2.1.0] - 2020-05-31

### Changed

- Navigation bar can now handle multilevel pages
- Updated phonenumbers to 8.12.4

### Fixed

- Removed unnecessary spaces at the start of the application form

### Removed

- Facebook app id since it is not needed for public facebook pages

## [2.0.1] - 2020-04-17

### Fixed

- Webpages that are migrated to sections don't take up the full witdh of the page
- Html and news blocks don't break when being converted

### Changed

- Updated wagtail to 2.7.2

## [2.0.0] - 2020-04-13

### Added

- Body and title fields in webpage and homepage are now accessible via wagtails api
- Added an image + text card block

### Changed

- Webpage and homepage blocks are reworked to allow a more simpler designing of webpages
- Updated django-simple-email-confirmation to 0.70
- Updated phonenumbers to 8.12.1
- Updated psycopg2-binary to 2.8.5

## [1.2.1] - 2020-02-22

### Fixed

- Uploaded files are now created with permissions 644 instead of 600
- Fix bug that caused text on banners to dissapear if the text was to long
- Fix bug that caused help text on image overlay to display unecessary text

### Changed

- Updated django to 2.2.10
- Updated phonenumber to 8.11.4
- Updated requests to 2.23.0
- Updated wagtailmedia to 0.5.0

## [1.2.0] - 2020-02-11

### Added

- Added wagtail media(videos and audio) to banners
- Added optional margin to two-grid column

### Removed

- Removed description from contact card

## [1.1.3] - 2020-02-06

### Fixed

- Fix a bug that caused applications with teams without logos to use another logo instead of the default logo
- Fixed so that the SSN validator can handle T-numbers and people born before 1990

### Changed

- Added text shadow to text in image overlay block
- Updated phonenumbers to 8.11.3

## [1.1.2] - 2020-01-28

### Fixed

- Fixed a bug which cause an application to be empty when applying with invalid references
- Added a missing database migration

## [1.1.1] - 2020-01-27

### Changed

- Updated phonenumbers to 8.11.2

## [1.1.0] - 2020-01-27

### Added

- Added possibility to add environment variables in dev environment
- Added validation on registration form
- Added contact information and references when inspecting an application
- Added utnarm.se as a allowed host

### Changed

- Extended createsuperuser so it gets a melos id
- Teams, roles and positions are now ordered alphabetically after their name
- Updated django-compressor to 2.4
- Updated django-libsass to 0.8
- Updated wagtail to 2.7.1
- Updated rules to 2.2
- Updated wagtailfontawesome to 1.2.1
- Updated django to 2.2.9

### Removed

### Fixed

- Fixed a bug with contact cards which caused an error
- Fixed an error that occured when searching for a role
- Fixed so that positions with status approved is shown when inspecting a position

## [1.0.2] - 2019-12-23

### Changed
Updated the text on the login page to be more clear

## [1.0.1] - 2019-12-23

### Fixed
Fixed bug that made event block hiding itself

## [1.0.0] - 2019-12-6

The migrations for this update requires that every table prefixed with `involvement` and `members` is truncated except for:
- `members_section`
- `members_section_studies`
- `members_studyprogram`


### Changed
- Changes to the admin permission system that depends on what role a user has.

The table below shows the permissions a user has depending on what role it has.
By default, the user only has the permissions inside its team.

Example: If the user is a board member, then that user has full control to modify any roles, positions and contact cards inside its own team.
Exception to applications where a board member can see and modify applications for all teams.

|               | Admin         | FUM                           | Board                 | Presidium             | Group Leader  | Engaged   |
| ------------- | ------------- | ----------------------------- | --------------------- | --------------------- | ------------- | --------- |
| Teams         | Full access   |                               |                       |                       |               |           |
| Roles         | Full access   | Board                         | Presidium             | Group Leader/Engaged  | Engaged       |           |
| Position      | Full access   | Board (appoint)               | Presidium             | Group Leader/Engaged  | Engaged       |           |
| Applications  | Full access   | Board/Presidium (all teams)   | Presidium (all teams) | Group Leader/Engaged  | Engaged       |           |
| Contact Cards | Full access   | Board/Presidium (all teams)   | Presidium             | Group Leader/Engaged  | Engaged       |           |

- Melos is now used to fetch user-information such as name, ssn and member status.
- Registering an account requires the SSN to exist in Melos.
- A user may now log in using both username or ssn.
- Firstname, Lastname, SSN, Registration Year and Study Program is no longer stored in Moores database and is instead fetched from Melos.
- Replaced Marvin to Bocken
- Upgrade dependencies

### Fixed
- Fixes several responsive layout problems.

### Added
- Event page where one can connect a Google Calendar, Facebook and Instagram to show upcoming events and image feeds.

## [0.11.0] - 2018-12-29
### Added
- Added a *mandate* system which tracks positions.
- Automatically create contact cards for appointed applications and vacant positions.
### Changed
- **Switch to a new hierarchical permission system (#254).**
- Upgrade dependencies to current versions.
- Improvements to the contact page design.
- Large python files are restructured into packages (models, forms, and views).
- Applicants can no longer change their application after submission.
- Old applications are removed after 7 days.
### Fixed
- Fixed crash caused by invalid `SelectMultiple`.
- Fixes several layout problems and responsive errors.
- User names are now unique independent of case.
### Removed
- Marvin Quotes.

## [0.10.1] - 2018-02-04
### Changed
- Upgrade dependencies to current versions

## [0.10.0] - 2017-10-02
### Changed
- Upgrade Django to version 1.11.5, Wagtail to version 1.12.2, compressor to version 2.2, Raven to version 6.2.1, and request to version 2.18.4.
- Font color of the overlay block. The new font is darker.
- Upgrade MaterializeCSS framework to version v0.100.2.
### Fixed
- The header padding of the open positions page in the involvement package

## [0.9.0] - 2017-07-27
### Added
- Block to embed Google Calendar fields
### Changed
- Changed the overturn field in the appointment window to work with person numbers instead of usernames
- Update request package to version 2.18.2

## [0.8.0] - 2017-07-21
### Added
- A panel in the Admin home showing all super users
- Add CheckboxSelectMultiple support to the materialize_field tag
- Add Contact Card Snippet model. This model represents the contact cards that can be added to different parts of the website and replace the Person Block
### Changed
- Updated MaterializeCSS to version 0.100.0
- Toast removal is executed using Materialize internal methods.
- Updated frontend to jQuery 3.2.1
- The logos blocks now also includes links for every logo
### Fixed
- Variable height of the responsive image block
### Removed
- Person Block, the functionality of this block has been replaced by the Contact Card Block.

## [0.7.0] - 2017-07-18
### Added
- A new page type, FormPage, to accommodate user made forms. The reactions of these forms are send to a given email address.
- A centered image format within the rich text editor.
## Changed
- The folder structure has changed to better reflect their functionality. `website/` has been renamed `src/` and `website/website` has been renamed `src/moore`.
- Improvements to the Google Drive block layout
- Height is now configurable for the responsive image block
### Fixed
- Materialize Textarea markup of the materialize_field tag
- The standard image formating rules in the rich text editor
- The bullet points of an unordered list in the paragraph block

## [0.6.0] - 2017-07-14
### Added
- Cron task to delete old non-appointed applications. (2 years after recruitment ends)
- Column based StreamBlock
- Person StreamBlock. This block looks like a contact card.
- Contact Page. A page for contact information
### Changed
- Old non-appointed applications are now hidden from the position inspection view
- All blocks in StreamFields have added to groups
- Production errors are no longer sent to the admin e-mails. (This was double with Sentry)
- Create more space in the navigation bar
### Fixed
- Release tag for Sentry logging

## [0.5.3] - 2017-07-11
### Added
- Sentry logging in production settings
### Changed
- Update to `wagtail` 1.11.1
- Update to `django` 1.11.3

## [0.5.2] - 2017-06-30
### Added
- Customizable site-specific footers
### Changed
- Update to `wagtail` 1.11
### Fixed
- Translation of sub-menus
- Ordering of the Google Form Index (This is now reverse order of the deadline)

## [0.5.1] - 2017-06-29
### Added
- Latest news block for StreamFields
### Fixed
- Fixes access to the Swedish HomePage banner text
- Align paragraph blocks using a container
- Translations for all page types in the top menu

## [0.5.0] - 2017-06-26
### Added
- First version of HomePage + some building blocks
- Add StreamField block for Google Drive
- Add StreamField block and collection pages for Google Forms
- Add News module
- Templated search page
- Pagination rendering in the materialize app
### Changed
- Update to `django` 1.11.2
- Update to `requests` 2.18.1
- Restructure the Noyce stylesheets
### Fixed
- Update GitHub button to new syntax (removes warning)
- Twitter links in the branding buttons
- New translation for application status
- Avatar overlay on Safari
- Update the translation of all translatable strings

## [0.4.1] - 2017-06-01
### Changed
- Update to `rules` 1.2.1 and `wagtail` 1.10.1
- Update to `requests` 2.17.3
### Fixed
- Do not show the error video on logout
- Fit the last apply button within the collapsible header
- Use short dates on involvement open positions page.
- Allow users that drafted an application to be appointed using overturn field.

## [0.4.0] - 2017-05-11
### Added
- Close button to close toast notifications.
### Changed
- Updated Wagtail to 1.10, including Django update to 1.11
- Updated the error pages to be more fun!
- Updated to Django 1.11.1, email-confirmation 0.22, and requests 2.14.2.
- Updated Materialize to 0.99
### Fixed
- Truncate the team name when screen gets too small.
- Use actual logo as default within the my applications page.
- Fix the double truncation of team names in the open positions page.
- Fixed the error 500 page needing a request.

## [0.3.4] - 2017-05-03
### Fixed
- Scaling issue on open positions.

## [0.3.3] - 2017-05-03
### Fixed
- Fix a big margin error on the open positions page.

## [0.3.2] - 2017-05-03
### Added
- Automated extensions of vacant positions. The election contact e-mail address will receive an e-mail.
### Changed
- Decreased the Marvin frequency.
### Fixed
- Position names are now contained by their container in the overview.
- The language and login buttons are now on the same height.
- The default team logo in the position view is now the actual UTN logo.
- Materialized fields no longer contain colons.

## [0.3.1] - 2017-04-27
### Fixed
- Access the material icon font through https.

## [0.3.0] - 2017-04-27
### Added
- Searching within involvement admin will now search more fields.
- A new form field type for person numbers
- Inspection view for Position, showing applicants
### Changed
- Switch to the materialize CSS/JS framework.
- Election contact e-mail has been moved to the Role model and has been labeled as such.
- Contact information of team members is now available in the Team inspection view.
### Removed
- Old migrations in the website app.
### Fixed
- Searching for positions within the admin interface will no longer cause an error.
- Allow person numbers to be "T-numbers".
- Several instances where dirrty wasn't triggered at the right time.
- Improved queries for loading positions.
- Disallow creating roles outside your team.

## [0.2.0] - 2017-04-07
### Added
- Inclusion and Exclusion of teams within a recruitment page.
- Inspection view for Teams to show the current members of a Team.
- A cron task to automate setting of access Group associated with Team.
### Changed
- Term of office is now visible in 'my applications'.
- Change the login button to be more visible.
### Removed
- Study program abbreviations.
### Fixed
- Update 'Account settings' translation for Swedish.
- Social Media Icons where not being displayed.

## [0.1.3] - 2017-04-06
### Fixed
- Use display value for degree for StudyProgram string method.
- Translate person number label where applicable
- Empty height of the organisational menu now matches the filled height.
- Initial selection of study is maintained when on section selection.
- Naming of position with double years if the span is over two years.
- Membership status is now shown when approving and appointing members.
- The role to string method is now correctly translated.

## [0.1.2] - 2017-04-01
### Added
- Section model, linked to study programs and users
- FontAwesome support within wagtail icons
### Changed
- Study has been removed from the registration page. Members will instead be
asked to extend their profile in the registration email.
### Fixed
- Confirmation emails not being sent.
- Updated translations
- Production: cross-domain cookies
- Makes the membership API more reliable

## [0.1.1] - 2017-03-30
### Added
- Notification on unconfirmed email addresses
- Membership status for all members. It checks against the UTN registry.
- Cron Tasks
### Changed
- Creating and editing positions is now sensitive to access rights.
- The logo model is now situated in the branding app.
- Phone number has been added to the registration form.
- Combine birthday and person number extension within the admin forms.
### Fixed
- Editing and creation rights in recruitment for officials
- Allow submitting an application without changing a draft
- Logos in the organisational menu now link to their given link
- The organisational menu is displayed correctly when no logos are available.
- The access rights for members of teams designated as an approval committee.

## [0.1.0] - 2017-03-27
### Added
- Django framework basics
- Wagtail CMS system
- Material design
- Member accounts and related information
- First version of the application system


[Unreleased]: https://github.com/UTNkar/moore/compare/v0.11.0...HEAD
[0.11.0]: https://github.com/UTNkar/moore/compare/v0.10.1...v0.11.0
[0.10.1]: https://github.com/UTNkar/moore/compare/v0.10.0...v0.10.1
[0.10.0]: https://github.com/UTNkar/moore/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/UTNkar/moore/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/UTNkar/moore/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/UTNkar/moore/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/UTNkar/moore/compare/v0.5.3...v0.6.0
[0.5.3]: https://github.com/UTNkar/moore/compare/v0.5.2...v0.5.3
[0.5.2]: https://github.com/UTNkar/moore/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/UTNkar/moore/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/UTNkar/moore/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/UTNkar/moore/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/UTNkar/moore/compare/v0.3.4...v0.4.0
[0.3.4]: https://github.com/UTNkar/moore/compare/v0.3.3...v0.3.4
[0.3.3]: https://github.com/UTNkar/moore/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/UTNkar/moore/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/UTNkar/moore/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/UTNkar/moore/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/UTNkar/moore/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/UTNkar/moore/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/UTNkar/moore/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/UTNkar/moore/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/UTNkar/moore/compare/8210c5175bcca87d9f012e49d090c8bec687c672...v0.1.0
