Andrew Maier and I have been [rethinking onboarding](https://18f.gsa.gov/2015/12/01/how-we-dramatically-improved-18fs-onboarding-process-in-3-months/) at 18F, and documentation keeps coming up.

Our coworkers are great at writing down what they learn in Slack, our chat program, because they're already in it all day. That knowledge doesn't always make it anywhere else, though, including our internal handbook.

So the handbook sometimes fell behind what people were saying in Slack, and new employees had a hard time finding the latest information.

I tried an experiment. I asked my 18F coworkers to tag any message *that every new 18F employee should know* with the :evergreen_tree: emoji.

Then I could search Slack for "has::evergreen_tree:" and pull up every tip and trick my coworkers thought mattered.

My coworker Micah Saul went a step further and wrote a small [command line utility](https://github.com/18F/emoji_search) that makes it easier to search Slack for a specific emoji.

Now the whole team can leave notes for future hires _without_ taking on _one more documentation chore._

It's worked well so far. More than 100 messages have been tagged with :evergreen_tree:, and we've added that material to the Handbook new hires get.

Next, we want to connect Micah's emoji finder to GitHub issues. New tagged messages would then land in a repo queue automatically, ready to be added to the handbook.
