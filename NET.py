from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView

from kivy.metrics import dp

import requests
import json
import time

from bs4 import BeautifulSoup


class APIExplorer(MDApp):

    def build(self):

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"


        root = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15)
        )


        title = MDLabel(
            text="NET",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height=dp(60)
        )


        self.url_input = MDTextField(
            text="https://api.github.com",
            hint_text="Enter URL",
            mode="rectangle",
            size_hint_y=None,
            height=dp(60)
        )


        buttons = MDBoxLayout(
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )


        fetch = MDRaisedButton(
            text="FETCH"
        )

        fetch.bind(
            on_press=self.fetch_data
        )


        clear = MDRaisedButton(
            text="CLEAR"
        )

        clear.bind(
            on_press=self.clear_output
        )


        buttons.add_widget(fetch)
        buttons.add_widget(clear)



        self.status = MDLabel(
            text="Status: Waiting",
            size_hint_y=None,
            height=dp(60)
        )


        self.output = MDLabel(
            text="Response will appear here",
            size_hint_y=None,
            valign="top",
            halign="left"
        )


        self.output.bind(
            texture_size=self.update_size
        )


        scroll = MDScrollView()

        scroll.add_widget(
            self.output
        )


        root.add_widget(title)
        root.add_widget(self.url_input)
        root.add_widget(buttons)
        root.add_widget(self.status)
        root.add_widget(scroll)


        return root



    def update_size(self, instance, size):

        instance.height = size[1]



    def fetch_data(self, instance):

        url = self.url_input.text.strip()


        if not url.startswith("http"):
            self.output.text = "Invalid URL"
            return


        try:

            start = time.time()


            response = requests.get(
                url,
                headers={
                    "User-Agent":
                    "Mozilla/5.0 NET"
                },
                timeout=15
            )


            elapsed = round(
                time.time() - start,
                3
            )


            content_type = response.headers.get(
                "content-type",
                ""
            )


            self.status.text = (
                f"Status: {response.status_code}\n"
                f"Type: {content_type}\n"
                f"Time: {elapsed}s"
            )



            # JSON
            if "json" in content_type.lower():

                try:

                    data = response.json()

                    output = json.dumps(
                        data,
                        indent=4
                    )


                except:

                    output = response.text



            # HTML
            elif "html" in content_type.lower():

                soup = BeautifulSoup(
                    response.text,
                    "html.parser"
                )


                title = (
                    soup.title.text
                    if soup.title
                    else "No title"
                )


                links = []

                for a in soup.find_all(
                    "a",
                    href=True
                ):
                    links.append(
                        a["href"]
                    )


                output = (
                    f"PAGE TITLE:\n{title}\n\n"
                    f"LINKS FOUND:\n"
                )


                for link in links[:30]:
                    output += f"{link}\n"



            # Other files/text
            else:

                output = response.text



            self.output.text = output[:15000]



        except requests.exceptions.Timeout:

            self.status.text = "Timeout"
            self.output.text = (
                "Website took too long to respond"
            )


        except requests.exceptions.ConnectionError:

            self.status.text = "Connection Error"
            self.output.text = (
                "Could not connect"
            )


        except Exception as e:

            self.status.text = "Error"
            self.output.text = str(e)



    def clear_output(self, instance):

        self.output.text = ""
        self.status.text = "Status: Cleared"



APIExplorer().run()