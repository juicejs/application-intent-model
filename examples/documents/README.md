# Document import (AIM 5.8)

[The model](./aim/documents/documents.aim) demonstrates a caller-supplied `file` Input, a document-reading Capability invoked by the business Contract, and a retained `file` on a Record. The provider binding is illustrative; the model prescribes no storage or parsing implementation.

The upload input is named `document`, while the retained source is named `source`: incoming documents and stored fields need not share names. Already-parsed text or a remote-source address would have its own appropriate input type.

See specification §3.7 and §13.9. This example has no View, so it owes no visual identity.
