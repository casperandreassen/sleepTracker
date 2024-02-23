// Follow this setup guide to integrate the Deno language server with your editor:
// https://deno.land/manual/getting_started/setup_your_environment
// This enables autocomplete, go to definition, etc.
import { html } from "https://deno.land/x/html/mod.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { Database } from "../schema.gen.ts";

console.log("Hello from Functions!");

function convertMilliSecondsToTimeString(milli: number): string {
  const hours = Math.floor((milli / (1000 * 60 * 60)) % 24);
  const minutes = Math.floor((milli / (1000 * 60)) % 60);
  return hours == 0
    ? `${minutes} minutes`
    : `${hours} hours and ${minutes} minutes.`;
}

Deno.serve(async (req) => {
  const authHeader = req.headers.get("Authorization")!;
  const supabaseClient = createClient<Database>(
    Deno.env.get("SUPABASE_URL") ?? "",
    Deno.env.get("SUPABASE_ANON_KEY") ?? "",
    { global: { headers: { Authorization: authHeader } } },
  );
  const user_id = (await supabaseClient.auth.getUser()).data.user?.id;

  if (!user_id) {
    return new Response("Could not get userid", { status: 404 });
  }
  const { data, error } = await supabaseClient.from("actions").select("*")
    .order("time").eq("user_id", user_id).limit(5);

  if (error) {
    return new Response(error.message, { status: 500 });
  }

  let statusString;
  if (data.length >= 1) {
    const lastTime = new Date(data[data.length - 1].time).getTime();
    const difference = convertMilliSecondsToTimeString(
      new Date().getTime() - lastTime,
    );
    const action = data[data.length - 1].action == "wake"
      ? "Awake for "
      : "Sleeping for ";
    statusString = action + difference;
  }

  const content = html`
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Activity Log</title>
    <style>
      body {
        background-color: #EEEEEE;
        font-family: Arial, Helvetica, sans-serif;
        margin: 0;
        padding: 0;
      }
      .list {
        margin: 20px 40px;
      }
      ul {
        list-style-type: disc;
        padding-left: 10;
      }
      li {
        margin-bottom: 10px;
      }
    </style>
  </head>
  <body>
    <div class="list">
      <h3>Activity Log</h3>
      <p>${statusString && statusString}</p>
      <ul>
        ${
    data.map((x) => `
          <li>${x.action} at ${
      new Date(x.time).toLocaleTimeString("nb-NO")
    }</li>
        `).join("")
  }
      </ul>
    </div>
  </body>
  </html>
  `;

  return new Response(
    content,
    { headers: { "Content-Type": "text/html" } },
  );
});

/* To invoke locally:

  1. Run `supabase start` (see: https://supabase.com/docs/reference/cli/supabase-start)
  2. Make an HTTP request:

  curl -i --location --request POST 'http://127.0.0.1:54321/functions/v1/get_report' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0' \
    --header 'Content-Type: application/json' \
    --data '{"name":"Functions"}'

*/
