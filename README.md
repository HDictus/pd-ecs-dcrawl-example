Dcrawls
=======

This was intended to be a simple example project for the pd-ecs framework: how its approach to entity-component systems could be used to make performant python games.

Ultimately, it demonstrated the failure of pd-ecs by having a dismal framerate with a trivial program.
pd-ecs tried to design for flexibility, so that you did not need to define object types, only attach and detach components, then retrieve entities with the appropriate components attached.
This led to some expensive concatenation operations which slow everything down a great deal.
It might lead to effective cache optimization for large numbers of entities - but clearly the overhead is prohibitive for games.

Before I do anything else in either project, I need to read up more about Data Oriented Design.
I probably need to rework pd-ecs so that it lets the developer specify how to store components, while offering them the flexibility to switch it up later.
At the moment I have too much on my mind for this.
Finish my PhD, my other game, and then take some time for this.