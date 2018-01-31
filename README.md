# Work at Olist

[Olist](https://olist.com/) is a company that offers an integration platform
for sellers and marketplaces allowing them to sell their products across
multiple channels.

The Olist development team consists of developers who loves what they do. Our
agile development processes and our search for the best development practices
provide a great environment for professionals who like to create quality
software in good company.

We are always looking for good programmers who love to improve their work. We
give preference to small teams with qualified professionals over large teams
with average professionals.

This repository contains a problem used to evaluate the candidate skills.
It's important to notice that satisfactorily solving the problem is just a
part of what will be evaluated. We also consider other programming disciplines
like documentation, testing, commit timeline, design and coding best
practices. 

Hints:

* Carefully read the specification to understand all the problem and
  artifact requirements before start.
* Check the recommendations and reference material at the end of this
  specification.


## How to participate

1. Make a fork of this repository on Github. If you can't create a
   public fork of this project, make a private repository
   (bitbucket offers free private repos) and add read permission for the 
   users [@osantana](https://bitbucket.org/osantana) and
   [@dvainsencher](https://bitbucket.org/dvainsencher) on project;
2. Follow the instructions of README.md (this file);
3. Deploy your project on a host service (we recommend
   [Heroku](https://heroku.com));
4. Apply for the position at our [career page](https://www.99jobs.com/olist)
   with:
   * Link to the fork on Github (or bitbucket.org);
   * Link to the project in a the deployed host service.


## Specification

You should implement a Python application that receives call detail records
and calculates monthly bills for a given telephone number.

This Python application must provide a HTTP REST API to attend the
requirements.


### 1. Receive telephone call detail records

There are many telecommunications platform technologies that can potentially
be clients of this system. Each one has its own communication flow. It's not
safe to believe that when an already sent record can be resent or retrieved
later. This context requires system flexibility in receiving information to
avoid record loss.

There are two call detailed record types: **Call Start Record** and **Call
End Record**. To get all information of a telephone call   you should use the
records pair. 

Call Start Record information:

* **record identifier**: Record unique identificator;
* **record type**: Indicate if it's a call start or end record;
* **record timestamp**: The timestamp of when the event occured;
* **call identifier**: Unique for each call record pair;
* **origin phone number**: The subscriber phone number that originated the
  call;
* **destination phone number**: The phone number receiving the call.
   
The Call End Record has the same information excepting **origin** and
**destination** fields.

The phone number format is *AAXXXXXXXXX*, where *AA* is the area code and
*XXXXXXXXX* is the phone number. The phone number is composed of 8 or 9
digits.


#### Examples

1. Call Start Record

```
{
  "id":  // Record unique identificator;
  "type":  // Indicate if it's a call "start" or "end" record;
  "timestamp":  // The timestamp of when the event occured;
  "call_id":  // Unique for each call record pair;
  "source":  // The subscriber phone number that originated the call;
  "destination":  // The phone number receiving the call.
}
```

2. Call End Record

```
{
   "id":  // Record unique identificator;
   "type":  // Indicate if it's a call "start" or "end" record;
   "timestamp":  // The timestamp of when the event occured;
   "call_id":  // Unique for each call record pair.
}
```


### 2. Get telephone bill 

To get a telephone bill we need two information: the subscriber telephone
number (required); the reference period (month/year) (optional). If the
reference period is not informed the system will consider the last closed
period. In other words it will get the previous month. It's only
possible to get a telephone bill after the reference period has ended.

The telephone bill itself is composed by subscriber and period
attributes and a list of all call records of the period. A call record
belongs to the period in which the call has ended (eg. A call that
started on January 31st and finished in February 1st belongs to February
period).

Each telephone bill call record has the fields:

* destination
* call start date
* call start time
* call duration (hour, minute and seconds): e.g. 0h35m42s
* call price: e.g. R$ 3,96


### 3. Pricing rules

The call price depends on fixed charges, call duration and the time of
the day that the call was made. There are two tariff times:

1. Standard time call - between 6h00 and 22h00 (excluding):
   * Standing charge: R$ 0,36 (fixed charges that are used to pay for the
     cost of the connection);
   * Call charge/minute: R$ 0,09 (there is no fractioned charge. The
     charge applies to each completed 60 seconds cycle).
  
2. Reduced tariff time call - between 22h00 and 6h00 (excluding):
   * Standing charge: R$ 0,36
   * Call charge/minute: R$ 0,00 (hooray!)

It's important to notice that the price rules can change from time to
time, but an already calculated call price can not change.


#### Examples

1. For a call started at 21:57:13 and finished at 22:10:56 we have:

   * Standing charge: R$ 0,36
   * Call charge: 
     * minutes between 21:57:13 and 22:00 = 2 (
     * price: 2 * R$ 0,09 = R$ 0,18
   * Total: R$ 0,18 + R$ 0,36 = R$ 0,54


## Project Requirements:

* Provide a working environment with your project (eg. Heroku)
* Use Python >= 3.5
* Choose any Python web framework you want to solve the problem
* Every text or code must be in English
* Use PEP-8 for code style
* Write the project documentation containing:
  * Description;
  * Installing and testing instructions;
  * Brief description of the work environment used to run this
    project (Computer/operating system, text editor/IDE, libraries, etc).
* Provide an API documentation (in english);
* Variables, code and strings must be all in English.


## Recommendations

* Write tests!
* Practice the [12 Factor-App](http://12factor.net) concepts;
* Use [SOLID](https://en.wikipedia.org/wiki/SOLID_(object-oriented_design))
  design principles;
* Use programming good practices;
* Use a good [Python Coding
  Style](http://docs.python-guide.org/en/latest/writing/style/);
* Use git best practices (https://www.git-tower.com/learn/git/ebook/en/command-line/appendix/best-practices),
  with clear messages (written in English);
* Be aware when modeling the database;
* Be careful with REST API details. They can bite you!

**Have fun!**
