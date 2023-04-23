import config

openai = "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"
twitch = "oauth:gfqscti223t5fdl0qrqc632vju8f49"
bearer = "eyJhbGciOiJSUzI1NiIsImtpZCI6Imluc18yTWtjQlhndjhpbEwxcGNDTnB3MXV5anF0azgiLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwczovL25hdC5kZXYiLCJleHAiOjE2ODA1NzY2ODMsImlhdCI6MTY4MDU3NjYyMywiaXNzIjoiaHR0cHM6Ly9jbGVyay5uYXQuZGV2IiwianRpIjoiMTU0ZDhlZmUyOGNlNzVkMDMwYTUiLCJuYmYiOjE2ODA1NzY2MTMsInNpZCI6InNlc3NfMk52WEZBZjR1dUxlRW9qeHpYdkdCaFltdFE0Iiwic3ViIjoidXNlcl8yTnZYRkVScEwzaG1BRjBQVG0xdmppS1NoMmsiLCJ1c2VyX2VtYWlsIjoiZHVmZm1hbjc5MTU0OTJAZ21haWwuY29tIiwidXNlcl9maXJzdF9uYW1lIjoiTmVvRGltIiwidXNlcl9pZCI6InVzZXJfMk52WEZFUnBMM2htQUYwUFRtMXZqaUtTaDJrIiwidXNlcl9sYXN0X25hbWUiOm51bGx9.NYL56iyhKr0ZVX3HtcUExsOCR7h-TIvY-wxoqg0Bm72_Z2hzvl1P6HJ4w2NTY1fOnTh-lf_WSjNd88JiqwGrR8oh3V-o1JH3xHF5GEy3jAQw5VQtjP737ihk1XBX-CrE75JQYXTTf8LeCo3qfwvHQHEWuK5YH3WYTl8JoQM31hhO6ELZSuK1nkHOdlnGR8jQenHD3NGwYCo0feEbcOuFE31uH4Og8t8u4KkyfM3hvbu9icas9EmWV1TGUILRa0BgaeGfxkdTfGHrXEZV5tLC9r1xvhKF2Vus-tMCkIR7VG6smS3QJNA7zWqFv0UxzHalPjoxzG0rcA3-XGt3UDNJCg"
url = "https://nat.dev/api/stream"
data = {
    "prompt": config.prompt_base,
    "models": [
        {
            "name": "openai:gpt-4",
            "tag": "openai:gpt-4",
            "provider": "openai",
            "parameters": {
                "temperature": 0.69,
                "maximumLength": 572,
                "topP": 1,
                "presencePenalty": 0,
                "frequencyPenalty": 0,
                "stopSequences": [

                ]
            },
            "enabled": True,
            "selected": True
        }
    ]
}
cookie = "__session=eyJhbGciOiJSUzI1NiIsImtpZCI6Imluc18yTWtjQlhndjhpbEwxcGNDTnB3MXV5anF0azgiLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwczovL25hdC5kZXYiLCJleHAiOjE2ODE2ODgyOTUsImlhdCI6MTY4MTY4ODIzNSwiaXNzIjoiaHR0cHM6Ly9jbGVyay5uYXQuZGV2IiwianRpIjoiMjk0NWNmNjRkYjljZGEwYTVjMjIiLCJuYmYiOjE2ODE2ODgyMjUsInNpZCI6InNlc3NfMk9IaTNzbjdnbDRwbjVNVTNxZUp0SlZnWnZjIiwic3ViIjoidXNlcl8yTnZYRkVScEwzaG1BRjBQVG0xdmppS1NoMmsiLCJ1c2VyX2VtYWlsIjoiZHVmZm1hbjc5MTU0OTJAZ21haWwuY29tIiwidXNlcl9maXJzdF9uYW1lIjoiTmVvRGltIiwidXNlcl9pZCI6InVzZXJfMk52WEZFUnBMM2htQUYwUFRtMXZqaUtTaDJrIiwidXNlcl9sYXN0X25hbWUiOm51bGx9.OHL2kOvq5FAZ76o-_TIkJJCqIyEQ5N7w_AHmByXTs8OTgAdP3Pvkj2Hy0scr38DS3TLXCkvXBQ2yn0uYLGJYQ4q__PJv-Zr_OS352p52DbDOTLDPDiMs3TNCRe7DQgzofN6lfWDUWX8UrHfnMZ1zV9swV5YxC_lSgjEfoNxaE9NadEDRBIV_jHrEyMlqKTAalUzWgS0aFWUCIHTDTGmywZZCasSuQnuWRQWu7LFLx0BkD4woD0vpN4Me1YGmPhDPf65AxrA-7cdR6G_3L3z0_vfyc16xhNYtVYTNQ0OEzKukcD_-BX2BSRQ0oOaICKqWqpyQ7DIfIBimvXObhGBK5A"