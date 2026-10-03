# Project Wave – Bottled Messages Application

## Project Description

Project Wave is a Django web application designed to facilitate interactive group experiences through digital "waves". A facilitator can create a wave for an event or session and invite participants to join it. Once participants have joined a wave, they can interact with the facilitator and with one another through different types of digital input.

The application is built around two main interaction types: **Bottle Exchange** and **Pulse Check**.

The Bottle Exchange allows participants to write messages which are exchanged between participants in the wave. The concept is inspired by the traditional idea of placing a message inside a bottle and sending it out to sea. The Pulse Check provides a different type of interaction, allowing participants to submit messages directly to the facilitator, those messages are listed on the screen for all to see.

The application provides separate functionality for two types of users: **Facilitators** and **Participants**. Facilitators can create and manage their waves, while participants join a specific wave and interact with the activities enabled by the facilitator.

A QR code is generated for each wave's participant page, allowing participants to access the relevant wave easily during an event.

The application was developed using Django and Bootstrap, with custom HTML, CSS and JavaScript used to create the application's interface and interactive functionality.

Two API solutions have been implemented for this project.


## Features

#### Feature 1 – Facilitator Registration and Authentication

Facilitators can create an account and log into the application.

After registering, facilitators are automatically logged into the application and redirected to their personal wave dashboard.

Authentication is used throughout the application to ensure that facilitators can only access and manage waves associated with their own account.

Django's built-in authentication functionality is used for login and logout, while a custom `WaveUser` model extends Django's `AbstractUser` to support the application's user types.


#### Feature 2 – Participant Registration for a Specific Wave

Participants register through a wave-specific registration URL, presented to them by the facilitator with the help of a unique QR code (I used an API for this function).

The wave ID is included in the registration URL, allowing the participant account to be associated directly with the relevant wave.

After successful registration, participants are automatically logged in and redirected to their wave.

Participants cannot access another participant's wave. The application checks the participant's stored `wave_id` against the requested wave ID before allowing access.


#### Feature 3 – Two Different User Types

The application distinguishes between two types of users, besides the superuser (myself):

* Facilitators
* Participants

The `WaveUser` model contains a `user_type` field which determines the user's role within the application.

This role-based structure allows the application to provide different functionality depending on the user's purpose.

Facilitators can create and present waves, while participants interact with the activities within the wave they have joined.


#### Feature 4 – Creating New Waves

Facilitators can create new waves from their dashboard.

When creating a wave, the facilitator can provide the relevant wave information through the `WaveForm`.

Each wave stores information including:

* Wave name
* Event date
* Facilitator
* Completion status
* Input type
* Moderation type
* Number of bottle releases
* Creation date

Once a wave has been created, it is associated with the facilitator who created it and appears in the facilitator's "My Waves" dashboard.

#### Feature 5 – QR Code Access to Waves

Each wave presentation page generates a QR code linking directly to the participant page for that wave.

The QR code is generated using the QRServer API.

The generated URL contains the relevant wave ID, meaning that participants can scan the QR code and be taken directly to the appropriate wave.

This feature is particularly useful for live events because participants do not need to manually enter a long URL.


#### Feature 6 – My Waves Dashboard

Facilitators have a dedicated dashboard displaying the waves they have created.

The dashboard displays:

* Wave name
* Group size
* Event date
* Completion status
* Input type
* Moderation type

The wave name acts as a link to the presentation area for that particular wave.

The dashboard also includes an "Add Wave" button, allowing facilitators to create additional waves.


#### Feature 7 – Bottle Exchange

The Bottle Exchange is one of the main interactive features of Project Wave.

When Bottle Exchange is enabled for a wave, participants can submit a message using the Bottle Exchange form. Facilitators can use a manual button to enable the forms to be sent to participants assigned to the wave (i.e. the session).

Each bottle stores information about its wave, sender, recipient, message, input type, creation time, release number.

The application uses a release number to keep track of different rounds of bottle exchanges.

This allows participants to send a new bottle when a new exchange round is released and prevents the same bottle from being repeatedly submitted within the same release.


#### Feature 8 – Receiving Bottle Messages

Participants can receive a bottle message from another participant within their wave.

The application checks the participant's wave, recipient ID, input type, and release number when looking for a received bottle.

This means that bottle messages are associated with a particular exchange round and intended recipient rather than simply being displayed as a general list of messages.

When a new bottle is available, the participant can view the received message through their wave page.


#### Feature 9 – Pulse Check

The second main interaction type is the Pulse Check.

When Pulse Check is enabled, participants can submit a message through the Pulse Check form. Facilitators can use a manual button to enable this.

Unlike the Bottle Exchange, the Pulse Check is directed towards the facilitator. The submitted message is therefore stored with the facilitator as the recipient.

Pulse Check messages are displayed in the facilitator's presentation view, allowing the facilitator to see messages submitted by participants during the session.


#### Feature 10 – Switching Between Bottle Exchange and Pulse Check

Facilitators can control which type of interaction is active for their wave.

The presentation page contains controls to:

* Enable Pulse Check
* End Pulse Check
* Enable Bottle Exchange
* End Bottle Exchange

JavaScript is used to update the interface immediately when the facilitator changes the active input type.

The selected input type is also sent to a Django API endpoint, which updates the corresponding wave in the database.

This allows the facilitator to change the activity during an ongoing session without needing to navigate away from the presentation page.


#### Feature 11 – Live Wave Input API

Project Wave includes an API endpoint used to update the active input type of a wave.

The presentation page sends a POST request containing the wave ID and the selected input type.

The Django view checks that:

1. The user is authenticated.
2. The user is a facilitator.
3. The request uses the POST method.
4. The wave belongs to the logged-in facilitator.

Only after these checks does the application update the wave's input type.

This provides the underlying functionality for switching between Bottle Exchange, Pulse Check, and no active input type.


#### Feature 12 – Presentation Mode for Facilitators

Facilitators have a dedicated presentation view for each wave.

The presentation page displays the wave information, QR code, and submitted Pulse Check messages.

It also provides the controls needed to enable or end Bottle Exchange and Pulse Check activities.

The presentation view is designed to be displayed during an event while participants interact with the wave through their own devices.


#### Feature 13 – Account Details Can Be Updated

Authenticated users can access their account details through the user menu.

The application provides separate account forms for facilitators and participants.

When account details are updated, the user's `updated_date` field is also updated.

A confirmation message is displayed after a successful account update.


#### Feature 14 – Password Reset

The application includes Django's password reset functionality.

Users can request a password reset by entering their email address.

The application includes dedicated pages for:

* Requesting a password reset
* Confirming that the reset email has been sent
* Entering a new password
* Confirming that the password has been successfully reset

This allows users to regain access to their account without requiring administrator intervention.


#### Feature 15 – Responsive Navigation

The application uses a responsive navigation structure.

On larger screens, the application displays a sidebar containing the main navigation.

On smaller screens, the sidebar can be opened using a navigation toggle button.

The toggle button includes an `aria-label` to clearly communicate its purpose to users of assistive technologies.


#### Feature 16 – Authenticated User Menu

Authenticated users can access a dropdown menu containing their username and account options.

The menu includes:

* My Profile
* Logout

Unauthenticated users are instead shown a Login button.

The navigation therefore adapts according to the user's authentication status.


#### Feature 17 – Wave-Specific Data Management

Each wave stores its own activity and participant-related information.

Bottle messages contain a reference to their wave, while participants also store the wave to which they belong.

This ensures that messages and participant activity remain associated with the correct session.

The application also stores a `join_order` for participants. This is intended to provide an incrementing participant position within each wave which can be used when determining how bottle messages are distributed.


#### Feature 18 – Bottle Release Tracking

The Wave model contains a `bottle_releases` field which keeps track of the number of bottle exchange releases completed by the facilitator.

Bottle messages store their own `release_number`.

This allows the application to distinguish between different rounds of bottle exchange activity and determine whether a participant has a new bottle available.


#### Feature 19 – Resources Area

The application includes a dedicated resources page.

This provides a separate area where supporting information and resources can be made available to users.


## Design choices

#### Colours

The application's visual design was developed around the concept of waves, bottles, and the ocean. 

Another important aspect behind this simplistic design was that the application's target audience is wide as I want the application to be used in various and numerous contexts (such as workshops, lectures, speeches, therapy sessions, etc.)

The use of consistent styling across the navigation, forms, buttons, tables, alerts, and wave presentation pages helps create a cohesive experience, and makes all users to focus on matters most: their input. 

Bootstrap is used for a number of standard interface components, while custom CSS is used to create the application's own visual identity.


#### Typography

Typography was selected with readability and simplicity in mind.

As the application is used during interactive sessions, information needs to remain clear and easy to read, particularly on the facilitator's presentation screen.


#### Images/Graphics

The readability and simplicity are reinforced through the use of a bottle image within the participant interface. This allows all users to focus on the input itself, thus encouraging participation.

When there is no currently active Bottle Exchange or Pulse Check interaction, the participant page displays a pixel-art image of an unopened bottle containing a message.

The application also uses a bottle-themed favicon to reinforce the visual identity of Project Wave within the browser.

The QR code is also styled to fit the overall team. 

#### Icons

Bootstrap Icons are used throughout the application.

Examples include:

* User/profile icons
* Navigation menu icons
* Login/logout icons
* Add/new-item icons

The icons provide additional visual cues and keep the interface consistent.

#### QR Code

The QR code was incorporated as both a functional and visual component of the facilitator presentation page.

Rather than requiring participants to manually enter a wave URL, the facilitator can display the QR code and allow participants to scan it using their mobile device.

This was particularly suited to the intended event-based use of the application.

## Development Process

#### Project planning

At the outset, I wanted to create an application that could support an interactive group experience rather than simply functioning as a standard messaging application.

The concept of a "wave" was used to represent an individual event or session. A facilitator creates the wave and participants subsequently join it.

The two interaction types were designed to provide different ways for participants to contribute.

The Bottle Exchange was developed around the idea of messages travelling between participants, while the Pulse Check was designed as a direct communication channel between participants and the facilitator.

The distinction between facilitator and participant accounts was therefore an important part of the initial application design.

I also wanted the application to work in a live event environment. This influenced the decision to create a dedicated facilitator presentation page and to provide QR-code access to the participant interface.

The project was developed using Django because its authentication system, forms, templates, database functionality, and security features provided a suitable foundation for the application.

#### Django Architecture

The application uses Django's template inheritance to maintain a consistent structure throughout the website.

The main authenticated layout contains the sidebar, top navigation, user account menu, feedback messages, main content area, and footer.

A separate logged-out base template is used for pages such as registration and password recovery.

Individual pages extend these base templates rather than duplicating the complete HTML structure.

The sidebar is also included as a separate template component.

This approach keeps common interface elements centralised and makes it easier to maintain consistency throughout the application.

#### Data Model

The application's main data structures are represented by the following models:

* `Wave`
* `Bottle`
* `WaveUser`

The `Wave` model represents a facilitator's event or session.

The `Bottle` model stores messages submitted through Bottle Exchange and Pulse Check activities.

The `WaveUser` model extends Django's `AbstractUser` and adds application-specific information such as user type, wave membership, follow-up requests, join order, and account update information.

An `Announcement` model is also included for storing wave-related prompts and requested input types.


#### Challenges Faced

One of the main development challenges was designing the application around two different user roles while maintaining a common authentication system.

Rather than creating completely separate user models, I used a custom `WaveUser` model based on Django's `AbstractUser`. The `user_type` field is then used to distinguish between facilitators and participants.

Another challenge was ensuring that participants could only access the wave they had registered for. The participant view checks the logged-in user's `wave_id` against the wave ID requested in the URL. If these do not match, the user is logged out rather than being allowed to access another participant's wave.

Managing the different interaction types also required additional logic. The same participant page needs to behave differently depending on whether the wave is currently running a Bottle Exchange, a Pulse Check, or neither.

Randomising the bottle exchange was another issue. To ensure that one user did not receive multiple bottled messages while another user did not receive any at all, I found it easier to rotate recipients based on their join order, rather than truly randomise who gets the message from who.

Each bottle stores a release number, while the wave stores the current number of releases. This allows the application to determine whether a participant has a new bottle available.

Another development consideration was the live facilitator controls. The presentation page needs to update the active input type without requiring a full page reload. JavaScript therefore sends the selected input type to the Django API endpoint, which updates the wave in the database. I had to work out how to build a JSON Django API and send to it from JavaScript using fetch.

Unit testing in Django proved harder than I expected. There were several problems with testing user session and the Django docs had multiple conflicting approaches.

Finding an API to use for AI moderation was unsuccessful. I evaluated 'moderationapi.com', 'cleanmod.dev', and 'openmoderation.com', but all of these were too expensive. I looked into self-hosting KoalaAI/Text-Moderation but the challenges involved were not possible for me to overcome in the time available.


## Deployed site

This site has been deployed to GitHub at the URL below:

[https://github.com/annakeil2/project-wave](https://github.com/annakeil2/project-wave)

Link to render.com deployment below:

[https://project-wave-p3id.onrender.com](https://project-wave-p3id.onrender.com)