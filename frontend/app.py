from dash import Dash, html, dcc, Input, Output
import dash
import dash_bootstrap_components as dbc
from flask import Flask

from lib.stores import app_stores
from lib.components.chat_components import render_navbar

server = Flask(__name__)


# Initialize the Dash app with Bootstrap
app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://use.fontawesome.com/releases/v5.15.4/css/all.css",
    ],
    suppress_callback_exceptions=True,
    server=server,
)

# Set the app layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        render_navbar(),
        dash.page_container,
        *app_stores,
    ],
    className="full-screen-div",
)

app.clientside_callback(
    """
    function(data) {
       // Delay the scroll update to let the DOM fully render the new message
       setTimeout(function(){
           const chatWindow = document.getElementById('chat-window');
           if (chatWindow) {
             chatWindow.scrollTop = chatWindow.scrollHeight;
           }
       }, 100);  // Adjust the delay as needed
       return '';
    }
    """,
    Output("scroll-output", "children"),
    Input("conversation-store", "data"),
)
if __name__ == "__main__":
    # app.run_server()
    app.run(
        debug=True, dev_tools_hot_reload=True
    )  # debug=False, host="0.0.0.0", port=80)
