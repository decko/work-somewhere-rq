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
   user [@tech-hiring](https://bitbucket.org/tech-hiring) on project;
2. Follow the instructions of README.md (this file);
3. Deploy your project on a host service (we recommend
   [Heroku](https://heroku.com) or [gigalixir](https://www.gigalixir.com));
4. Apply for the position at our [career page](https://www.99jobs.com/olist)
   with:
   * Link to the fork on Github (or bitbucket.org);
   * Link to the project in a the deployed host service.


## Specification

You should implement an application that receives call detail records
and calculates monthly bills for a given telephone number.

There are a plenty of telecommunications platform technologies that will
consume this application. Some of them have weird behaviours when something
goes wrong. That said it's not safe to believe in received data correctness,
consistency nor expect some order in their requests. The application should
have flexibility in receiving information to avoid record loss or inconsistency.

This application must provide a HTTP REST API to attend the
requirements.


### 1. Receive telephone call detail records

There are two call detailed record types: **Call Start Record** and **Call
End Record**. To get all information of a telephone call you should use the
records pair.

Call Start Record information:

* **record type**: Indicate if it's a call start or end record;
* **record timestamp**: The timestamp of when the event occured;
* **call identifier**: Unique for each call record pair;
* **origin phone number**: The subscriber phone number that originated the
  call;
* **destination phone number**: The phone number receiving the call.

The Call End Record has the same information excepting **origin** and
**destination** fields.

The phone number format is *AAXXXXXXXXX*, where *AA* is the area code and
*XXXXXXXXX* is the phone number. The area code is always composed of two digits
while the phone number can be composed of 8 or 9 digits.


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

1. For a call started at 21:57:13 and finished at 22:17:53 we have:

   * Standing charge: R$ 0,36
   * Call charge:
     * minutes between 21:57:13 and 22:00 = 2
     * price: 2 * R$ 0,09 = R$ 0,18
   * Total: R$ 0,18 + R$ 0,36 = R$ 0,54


### 4. Sample data
Insert the following calls to your app after it is deployed to a working environment (eg. Heroku, gigalixir). This sample data will be used in your evaluation, so do this as the last step before submitting the project.

The following phone calls have been made from the number 99 98852 6423 to 99 3346 8278 (whitespaces are used here only for readability purposes, the phone numbers formats have been specified on a previous section).
* call_id: 70, started at 2016-02-29T12:00:00Z and ended at 2016-02-29T14:00:00Z.
* call_id: 71, started at 2017-12-11T15:07:13Z and ended at 2017-12-11T15:14:56Z.
* call_id: 72, started at 2017-12-12T22:47:56Z and ended at 2017-12-12T22:50:56Z.
* call_id: 73, started at 2017-12-12T21:57:13Z and ended at 2017-12-12T22:10:56Z.
* call_id: 74, started at 2017-12-12T04:57:13Z and ended at 2017-12-12T06:10:56Z.
* call_id: 75, started at 2017-12-13T21:57:13Z and ended at 2017-12-14T22:10:56Z.
* call_id: 76, started at 2017-12-12T15:07:58Z and ended at 2017-12-12T15:12:56Z.
* call_id: 77, started at 2018-02-28T21:57:13Z and ended at 2018-03-01T22:10:56Z.


## Project Requirements:

* Provide a working environment with your project (eg. Heroku, )
* Application must be written in Python, Elixir or Go.
* Python
  * Use Python >= 3.5
  * Choose any Python web framework you want to solve the problem
  * Use PEP-8 for code style
  * [Python Coding Style](http://docs.python-guide.org/en/latest/writing/style/)
* Elixir
  * Elixir >= 1.6.5
  * Phoenix >= 1.3.0
  * [Elixir Style Guide](http://elixir.community/styleguide)
* Go
  * Go >= 1.10
  * [Effective Go](https://golang.org/doc/effective_go.html)
* Every text or code must be in English
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
* Use git best practices (https://www.git-tower.com/learn/git/ebook/en/command-line/appendix/best-practices),
  with clear messages (written in English);
* Be aware when modeling the database;
* Be careful with REST API details. They can bite you!

**Have fun!**
