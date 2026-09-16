# Authentication

Authentication and credentials are host-owned. Web, iOS, Android, and Studio
use their platform-appropriate login and credential storage. Credentials stay
outside game packages, snapshots, and creator source.

The shared Rust app runtime can build requests and interpret responses for
selected account features, but it does not own an HTTP runtime, login SDK,
access token, refresh token, or cookie. Hosts execute HTTP effects and return
status/body results to the app runtime.

Studio's current sign-in flow opens the existing web login in a browser,
receives a one-time code through a loopback callback, verifies state, and
exchanges the code for native tokens. Tokens remain in Studio memory for the
current slice; persistent OS keychain storage is a future hardening step.
Local project creation, asset import, preview, and validation do not require
sign-in.

Server checks remain authoritative for authentication, age eligibility,
uniqueness, moderation, and account mutations. Client validation exists for
useful feedback and is not a security boundary.
