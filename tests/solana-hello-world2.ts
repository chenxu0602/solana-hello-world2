// import * as anchor from "@coral-xyz/anchor";
// import { Program } from "@coral-xyz/anchor";
// import { SolanaHelloWorld2 } from "../target/types/solana_hello_world2";

// describe("solana-hello-world2", () => {
//   // Configure the client to use the local cluster.
//   anchor.setProvider(anchor.AnchorProvider.env());

//   const program = anchor.workspace.solanaHelloWorld2 as Program<SolanaHelloWorld2>;

//   it("Is initialized!", async () => {
//     // Add your test here.
//     const tx = await program.methods.initialize().rpc();
//     console.log("Your transaction signature", tx);
//   });
// });


import * as anchor from "@project-serum/anchor";
import { Program } from "@project-serum/anchor";
import { SolanaHelloWorld2 } from "../target/types/solana_hello_world2";
import * as assert from "assert";

describe("solana-hello-world2", () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  // const program = anchor.workspace.SolanaHelloWorld as Program<SolanaHelloWorld2>;
  const idl = JSON.parse(
    require("fs").readFileSync("./target/idl/solana_hello_world2.json", "utf8")
  );

  const programId = new anchor.web3.PublicKey("Ea1ASvNNxsFJ97M6erEzo8CiUzHx2H78oZy1WHMGGuim");
  const program = new anchor.Program(idl, programId, provider);


  // it("Can create a message", async () => {
  //   const message = anchor.web3.Keypair.generate();
  //   const messageContent = "Hello World";
  //   await program.rpc.createMessage(messageContent, {
  //     accounts: {
  //       message: message.publicKey,
  //       author: provider.wallet.publicKey,
  //       systemProgram: anchor.web3.SystemProgram.programId,
  //     },     
  //     signers: [message],
  //   });

  //   const messageAccount = await program.account.message.fetch(message.publicKey);
  //   log.info(messageAccount);

  //   assert.equal(messageAccount.author.toBase58(), provider.wallet.publicKey.toBase58());
  //   assert.equal(messageAccount.content, messageContent);
  //   assert.ok(messageAccount.timestamp);
  // });

  it("Can create and then update a message", async () => {
    const message = anchor.web3.Keypair.generate(); 
    const messageContent = "Hello World";
    // await program.rpc.createMessage(messageContent, {
    //   accounts: {
    //     message: message.publicKey,
    //     author: provider.wallet.publicKey,
    //     systemProgram: anchor.web3.SystemProgram.programId,
    //   },
    //   signers: [message],
    // });

    const updatedMessageContent = "Solana is cool!";
    await program.rpc.updateMessage(updatedMessageContent, {
      accounts: {
        message: message.publicKey,
        author: provider.wallet.publicKey,
        systemProgram: anchor.web3.SystemProgram.programId,
      },
    });

    const messageAccount = await program.account.message.fetch(message.publicKey);
    assert.equal(messageAccount.author.toBase58(), provider.wallet.publicKey.toBase58());
    assert.notEqual(messageAccount.content, messageContent);
    assert.equal(messageAccount.content, updatedMessageContent);
    assert.ok
  });
});

