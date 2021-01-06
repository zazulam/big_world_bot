# Big World Bot
This bot is a little side project to add some flavor in our discord server.

## Some useful features:
* Invite Tracking
  * If a member of the server creates an invite and has someone join from that it will search for a role named after the inviter and assign that role to the new joinee, if no role is found then one will be created. This allows for certain additional commands to view 'ancestors/families of members within the server.
* Question Polling
  * Adds the appropriate reactions for questions asked i.e. :thumbsup:, :thumbsdown:, 🤷‍♀️.
* Role Assignment
  * Allows members to assign certain roles to themselves, mainly the based ***Among Us*** colors.
* Game Headcount
  * Sends a message to the server with gif of the game in question and the same reactions as the question polling. When the number of :thumbsup:s reach the number requested +1(to account for the bot's :thumbsup:) it will notify the channel and tag all those who liked the headcount request. There is a ttl for the headcount, ~ 2 hours.
* Generic Invite
  * (requires 1 invite to be create that never expires) This is meant for dropping in the interwebz, those who join from this invite as randoms. They will only have access to reaction to messages and would be required to go through a quiz in order to be able to participate in the server. Currently there is only 1 question where any answer is regarded as correct, once they pass this their role will change from random to wildling and will be able to interact more within the server. This feature is to be used for accepting code of conduct/quizing newcomers on various topics to gain some insight on the types of members they might be. 
* Family
  * Uses the roles generated from the **Invite Tracker** to create a node graph of the member passed(red node) connected to their parent (inviter) and their children (invitees).
  Example: ***!family zazu***
  ![image](https://cdn.discordapp.com/attachments/759558589764599849/796179997709828096/family_zazu.png)
* Bigworld
  * Similar to the family command but goes through the server members who are connected which would lead back to the server owner(red node). **Note** Does not account for wildlings.
  Example: ***!bigworld***
  ![image](https://cdn.discordapp.com/attachments/759558589764599849/796181870424358962/bigworld_Noonz.png)

## Some not-so-useful, but playful features:
* Speak
  * This is just some fun/random command that is used during game nights that would act as a typical soundboard for the right occasions.

___
 
## Install & build:
### requirements:
* Python 3.8.x or higher
* A discord bot with permissions to manage server, intents, roles, view channels, all text permissions, connect & speak for voice permissions
* An API token for the Tenor API to retrieve gifs
  
