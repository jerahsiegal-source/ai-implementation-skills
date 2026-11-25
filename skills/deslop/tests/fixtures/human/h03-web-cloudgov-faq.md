Four weeks ago, we [announced cloud.gov](https://18f.gsa.gov/2015/10/09/cloud-gov-launch/), a new platform that will enable small federal teams to rapidly develop and deploy web services with best-practice, production-level security and scalability. The platform will also help agencies reduce the work required to comply with federal security regulations.

Currently, we’re running a small pilot program to prepare to open up [cloud.gov](https://cloud.gov) to all federal agencies. In the meantime, we’d like to lay out some more details about the project and answer some of the most common questions since we announced cloud.gov.

## What is included in cloud.gov?

cloud.gov includes a Platform-as-a-Service (PaaS) specifically built for government, based on the open source [Cloud Foundry](https://www.cloudfoundry.org/). It provides a secure, scalable platform for teams to build and host their application or website. It can help development teams work faster and cheaper by handling much of their deployment complexity.

cloud.gov also includes an open source product called [**Compliance Masonry**](https://github.com/18F/compliance-masonry). Compliance Masonry assists in assembling the documentation necessary for federal services to comply with Federal Information Security Management Act (FISMA) standards and agency-specific Authority to Operate (ATO) requirements. We’re using Compliance Masonry to gain the ATO for cloud.gov itself, and will provide our materials in a form that will greatly reduce the staff time required to prepare the ATO documentation for any app deployed on cloud.gov. We will expand Compliance Masonry’s role to support continuing assurance for deployed applications.

## Tell me more about the Platform-as-a-Service concept

Here’s a presentation that explains how cloud.gov’s PaaS can help free your staff to spend more time conquering problems that are unique to your agency and less time on regulatory compliance.

## Why would an agency want to use cloud.gov?

Hosting applications in the cloud does not automatically solve all the infrastructure problems that agencies face. It eliminates a lot of the concerns around managing data centers, but exposes the need for a new cloud operations skillset that is not yet widely available in government. The cloud.gov platform bundles up the skills of 18F’s operations experts and offers them as a package to federal agencies. Using cloud.gov will help you **improve your security** and **ease the federal compliance process**.

## How does cloud.gov improve security?

cloud.gov deploys all apps on a hardened operating system image that is tightly audited for compliance with federal standards. We regularly scan and audit the platform itself as well as applications running on it for vulnerabilities. We apply security updates to the underlying software stacks on a regular basis without interrupting application availability. The cloud.gov deployment itself is publicly documented and subject to scrutiny from all corners. Improvements in cloud.gov result in improved security for all apps running on top of it.
