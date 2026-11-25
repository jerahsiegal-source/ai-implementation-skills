Four weeks ago we [announced cloud.gov](https://18f.gsa.gov/2015/10/09/cloud-gov-launch/), a new platform for small federal teams. It lets them build and launch web services quickly, with production-level security and scaling. It will also cut down the work agencies do to meet federal security rules.

Right now we're running a small pilot while we get ready to open [cloud.gov](https://cloud.gov) to every federal agency. Until then, here are more details about the project and answers to the questions we've been asked most since the announcement.

## What is included in cloud.gov?

The first piece is a Platform-as-a-Service (PaaS) built for government. It's based on the open source [Cloud Foundry](https://www.cloudfoundry.org/). Teams can build and host their apps or websites on it, and it's secure and can scale. It takes care of much of the deployment work, so development teams can move faster and spend less.

The second piece is an open source tool called [**Compliance Masonry**](https://github.com/18F/compliance-masonry). It helps put together the paperwork federal services need to meet the Federal Information Security Management Act (FISMA) standards and each agency's Authority to Operate (ATO) requirements. We're using it to get the ATO for cloud.gov itself. We'll share those materials in a form that should save a lot of staff time when you prepare ATO paperwork for any app running on cloud.gov. Later, Compliance Masonry will also help with ongoing security checks for apps after they launch.

## Tell me more about the Platform-as-a-Service concept

This presentation shows how cloud.gov's PaaS lets your staff spend less time on regulatory compliance and more time on the problems only your agency has.

## Why would an agency want to use cloud.gov?

Moving apps to the cloud doesn't fix every infrastructure problem an agency has. You no longer have to run data centers, but you now need people who know how to run cloud operations, and that skill is still rare in government. cloud.gov packages what 18F's operations experts know and offers it to federal agencies. It will help you **improve your security** and **ease the federal compliance process**.

## How does cloud.gov improve security?

Every app on cloud.gov runs on a hardened operating system image that is closely checked against federal standards. We regularly scan and audit the platform and the apps on it for weak spots. We also install security updates to the software underneath on a regular schedule, and apps stay up while we do it. How cloud.gov is set up is documented in public, so anyone can examine it. When we improve cloud.gov, every app running on it becomes more secure.
