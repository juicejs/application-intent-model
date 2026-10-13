# Who does the work, and who may (AIM 5.10)

[The model](./aim/refunds/refunds.aim) is a small business process: a refund at the till. Its steps say in words who does them — "The cashier checks the receipt" — and those words are for the reader. Who performs each step is declared by edges: the `Cashier` and the `StoreManager` each `invokes` the operations they do, and every step invokes one of those operations.

Who *may* do it is named the same way: each operation's `### Authz` names its roles by address in backticks — `` `#Persona:StoreManager` `` — so the store manager may pay a refund out, though the cashier is the one who does. Several named roles are alternatives: any one of them may.

The words could be in any language, with any article and in any order — "Die Kassiererin prüft den Bon" reads the same — because no tool reads a performer or a permission out of a sentence. A step done by someone other than the Flow's performer invokes an operation its performer `invokes`.

See specification §7.3, §7.4 and §13.11. This example has no View, so it owes no visual identity.
