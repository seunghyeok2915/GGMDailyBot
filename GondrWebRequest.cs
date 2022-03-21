using System;
using System.IO;
using System.Net;
using System.Text;
using System.Text.Json;

namespace Examples.System.Net
{
    public class TokenData
    {
        public string token_type { get; set; }
        public int expires_in { get; set; }
        public string access_token { get; set; }
        public string refresh_token { get; set; }
    }
    public class DateData
    {
        public string date { get; set; }
    }
    public class WebRequestPostExample
    {
        public static void Main(string[] args)
        {
            if (args[0] == "SaveToken") //아이디 비번 
            {
                string token = GetToken(args[1], args[2]);

                Console.Write(token);
            }
            else if (args[0] == "WriteDaily") //토큰 팀넘버 내용
            {
                string token = "Bearer " + args[1];
                string teamNum = args[2];
                string content = "";
                for (int i = 3; i < args.Length; i++)
                {
                    content += args[i];
                    content += " ";
                }

                string date = GetDate(token);

                var result = WriteDaily(teamNum, content, date, token);

                Console.Write(result);
            }
            else
            {
                Console.Write("ERROR");
            }

        }

        private static string GetToken(string email, string password)
        {
            WebRequest request = WebRequest.Create("http://ggm.gondr.net/api/login");
            request.Method = "POST";

            string postData =
@"{{
  ""email"": ""{0}"",
  ""password"": ""{1}""
}}";
            byte[] byteArray = Encoding.UTF8.GetBytes(string.Format(postData, email, password));

            request.ContentType = "application/json;charset=UTF-8";
            request.ContentLength = byteArray.Length;
            request.Headers["Referer"] = "http://ggm.gondr.net/user/login";

            Stream dataStream = request.GetRequestStream();
            dataStream.Write(byteArray, 0, byteArray.Length);
            dataStream.Close();

            try
            {
                WebResponse response = request.GetResponse();
                string json = null;
                using (dataStream = response.GetResponseStream())
                {
                    StreamReader reader = new StreamReader(dataStream);
                    string responseFromServer = reader.ReadToEnd();
                    json = responseFromServer;
                }

                response.Close();

                TokenData result = JsonSerializer.Deserialize<TokenData>(json);
                return result.access_token;
            }
            catch (Exception)
            {
                return "BAD";
                throw;
            }
        }

        private static string GetDate(string token)
        {
            string json = null;
            WebRequest request = WebRequest.Create("http://ggm.gondr.net/api/server_now");
            request.Headers["Authorization"] = token;

            try
            {
                WebResponse response = request.GetResponse();

                using (Stream dataStream = response.GetResponseStream())
                {
                    StreamReader reader = new StreamReader(dataStream);
                    string responseFromServer = reader.ReadToEnd();
                    json = responseFromServer;
                }

                response.Close();

                DateData result = JsonSerializer.Deserialize<DateData>(json);

                return result.date;
            }
            catch (Exception)
            {
                return "BADTOKEN";
                throw;
            }
        }

        public static string WriteDaily(string teamNum, string content, string date, string token)
        {
            WebRequest request = WebRequest.Create("http://ggm.gondr.net/api/team/record/daily");
            request.Method = "POST";

            string postData =
@"------WebKitFormBoundaryzmxvKva0sJA3uSQ0
Content-Disposition: form-data; name=""team""

{0}
------WebKitFormBoundaryzmxvKva0sJA3uSQ0
Content-Disposition: form-data; name=""content""

{1}
------WebKitFormBoundaryzmxvKva0sJA3uSQ0
Content-Disposition: form-data; name=""record_day""

{2}
------WebKitFormBoundaryzmxvKva0sJA3uSQ0--";
            byte[] byteArray = Encoding.UTF8.GetBytes(string.Format(postData, teamNum, content, date));

            request.ContentType = "application/x-www-form-urlencoded";
            request.ContentLength = byteArray.Length;
            request.ContentType = "multipart/form-data; boundary=----WebKitFormBoundaryzmxvKva0sJA3uSQ0";
            request.Headers["Authorization"] = token;
            request.Headers["Host"] = "ggm.gondr.net";
            Stream dataStream = request.GetRequestStream();
            dataStream.Write(byteArray, 0, byteArray.Length);
            dataStream.Close();

            try
            {
                WebResponse response = request.GetResponse();
                using (dataStream = response.GetResponseStream())
                {
                    StreamReader reader = new StreamReader(dataStream);
                    string responseFromServer = reader.ReadToEnd();
                }

                response.Close();
                return "OK";
            }
            catch (Exception)
            {
                return "BADTOKEN";
                throw;
            }

            
        }
    }
}
