import java.io.File;
import java.net.URL;

public class I {
    private URL url;

    public URLFileOpener(String address) {                                                                     
        try {                                                                                                  
            this.url = new File(address.replace("/", File.separator)).toURI().toURL();                         
            new Here("Unit", 34).given(address, "/home/liuyu").given(File.separator, "/").checkEq(this.url, "URL1.xml");                                                                                                     
        } catch (MalformedURLException e) {                                                                    
            throw new RuntimeException(String.format("THIS SHOULD NOT HAPPEN: error while forming URL from path '%s'", address), e);                                                                                         
        }                                                                                                      
    }
}
