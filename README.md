# daily-fantasy
Data science and analysis of fantasy football games. Predictive modeling for daily fantasy contests
In short, we are trying to solve the classic knapsack problem with some restraints. We are given a salary cap, which is 
knapsack of set capacity. Each item we are choosing is a player we are adding to our roster, the player has a projected 
points, and salary cost, both values determined by the contest and vendor. In addition to the salary cap constraint, a 
proper fantasy roster must have players that fulfill the following position restrains:
* 1 quarterback (QB)
* 2 wide receivers (WR)
* 2 running backs (RB)
* 1 tight end (TE)
* 1 flex (WR/RB/TE) <u>this could get tricky</u>
* 1 kicker (K) not part of the model
* 1 defense (DEF) not part of the model

### High-level objectives
1. Use existing fantasy data to make base projections for a player's performance
2. Integrate the player's position, their team's performance at that position, the opponent team's performance against 
that position, and home vs. away advantage to produce an updated projection
3. Use the player's salary cost from a daily fantasy contest site to construct a roster given the salary constraints of 
the contest

#### Tasks
1. Create scripts to collect existing data and output merged data table
2. Create scripts to collect contest-level information from Draftkings, Fanduel, etc...
3. Train base model on existing data, use running average (last 5-7 weeks) as projection
4. Improve model on a weekly basis using the data from that week's games
5. Decide how to handle injury, durability, reliability, etc...

### Definitions
* Actual points scored: The number of points a player scored in week X of year Y playing for team A against team B
* Projected points: The number of points a player is projected to score by a given contest
* Player Salary/Cost: The in-game dollar amount it will cost to roster a given player
* Salary Cap/Limit: The maximum in-game dollar amount someone is allowed to spend on their roster
* Player (position) rank: The rank of a given player against others of his position based on the points scored over a 
given time period, or number of games.
* Opposing team: Identity of the opposing team of a given player
* Opposing team rank vs. position: The rank of the opposing team against the position of a given player (formula TBD)
* Team position-specific offensive rank: The position-specific offensive rank of the team a given player is on (formula TBD)


Past data, existing data:
* Fantasy results (yards, rec, targets, rush att, points scored)
* Base projection: projected points scored using only existing data, meant to serve as a proxy to the projected points 
as provided by the contest.

Real-time data, contest data, post-contest data:
* Player name, projected points, home vs. away, opponent (and their rank vs. pos), salary cost
* Actual points-per-dollar: After the contest, the number of points scored divided by the dollar cost
* Projected points-per-dollar: Before the contest, the project number of points divided by the dollar cost
* Actual - Projected: The difference between the actual number of points scored and the projected (ours or theirs)

### Caveats and Pitfalls
* No access to historical player projection or player cost data, this will be something we need to start collecting
once the games begin.

### Pre-season Activities
* Train base model (depends only on the player and their past performances, produces predictions or projected points 
scored independent of the opponent)
* Develop software (automation or work routines) to handle the following activities:
    * Scrape contest-level information from vendor (Draftkings, Fanduel, Yahoo, etc...)
    * Incorporate contest-level information into our model
    * Produce candidate rosters by solving the knap-sack problem with item-class count restrictions
    * Determine the top X rosters for submission