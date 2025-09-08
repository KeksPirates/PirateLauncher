# HOW TO OBTAIN & SET YOUR RUTRACKER SESSION COOKIE

1. Go to [rutracker.org](https://rutracker.org) and log in to your account.
2. Open your browser's Developer Tools (usually by pressing `F12` or `Ctrl+Shift+I`).
3. Navigate to the **Storage** or **Application** tab, then find **Cookies** for rutracker.org.
4. Locate the cookie named `bb_session` and copy its value.
5. Create a file named `.env` in the project root directory.
6. Add the following line to your `.env` file, replacing `{cookie}` with your copied value:

   ```
   bb_session={cookie}
   ```

7. Save the `.env` file.

Your session cookie is now set up for use with the Server.