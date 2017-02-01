ffmddb Use Case Scenario
========================

`ffmddb` was born from the idea that the best tool for editing a textfile is a text editor, and yet even text files benefit from managed metadata and relations between objects, as shown by a case study:

    I've been on the 'net for well over twenty years now, and over that period of time, I've amassed hundreds of log files. Some are notes, some are important conversations that led to relationship, some are inane conversations with individuals who have since passed away.

    In that time, I've run through several different organizational schemes, databases, and projects to manage these files. I wanted the organizational benefits of a relational database, the freedom of a document database, and the flexibility of editing the files by hand in whatever editor I choose. Finally, I wanted the ability to keep the files in a repository.

For the above problem space, the relation solution would be:

* A table of participants (name, about)
* A table of logs (name, text, date)
* A mapping table (log, participant)

In `ffmddb`, that maps to:

* A folder of participant files, text files with any document data, named after the participant
* A folder of log files, text files with any document data, and metadata containing a list of participants and the date of the log
* An index file containing mapping between logs by participant for faster queries

The same data and relations are represented, but in a format easily edited in any text editor, easily readible or served from something like Jekyll, and easily stored in a VCS repo. The goal is not speed, but flexibility for manually interfacing with smaller datasets.
