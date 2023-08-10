# Problem

## Goal: Score property to support the decision of user making capital gains-optimal investments
- Given a user-selected location, present properties in the location, that are likely to perform better, relative to other properties in the given location, not relative to all locations in Australia.
- **Stretch goal**: give interpretations of the reasons properties are selected, according to some pre defined criteria. 
- **Stretch goal**: make the selection conditional on not just location, but also other criteria the user might be interested in. Ie “off street parking”


## Customer: property investors, first time buyer, 30-40 yrs old, 150k+ income pa. 20+ yrs full-time
- Desires passive income for retirement (30+ yrs), maximise capital gains.
- Has some education on property investment. Ie is familiar with well known factors to property valuations & expected performance. 

## Existing solution
- Research properties on the marketplace - based on own criteria
  - Domain, realestate.com
  - Call real estate agents 
  - Inspect properties, neighbourhoods 
- Engage buyers agent - to find a property
- Manual data driven techniques, with expert advice sourced from multiple sources.

## Pain points of existing solution:
- Real estate agents have an agenda.
- Volume of data to manually analyse to get a desired level of confidence takes a lot of effort to process.
- Because the market always changes, the capacity a user has to analyse means there is a cap to the level of confidence a user can have before market conditions drift enough to make analyses outdated.
- Combining data types, like distances and dollars, is not a data driven approach. The user has to intuitively weight importance of different data types.
- Scope of candidate solutions for an investment decision makes it hard to know how close you are to the optimal decision. Ie, if a user had seen 50% of all possible properties, they’d be comfortable to be decisive after that. But it would be rare to see even an order of magnitude lower than that proportion, for a given location.

## Evidence
- 1995-2015 gives 10.5% Read the Long-Term Investing Report here
- 3 weeks to 3 months to search for a property: https://www.realestate.com.au/advice/how-long-should-property-research-take/#:~:text=“A%20buyer%20will%20know%20when,or%20the%20decision%2Dmaking.”

## Unknowns


# Success / Definition of Done
- Properties served have 95% confidence of being in the top quartile of ROI over a 25 year period. As evaluated on past performance, conditional on yet to be agreed upon assumptions the rational typical user would make (I.e. macro economic theories like growth in income = growth in predisposition to spend that income on property ‘desirability’).
- Above performance works for 3+ “locations” roughly the size of north Brisbane, including north Brisbane.
