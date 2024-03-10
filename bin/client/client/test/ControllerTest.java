import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import javax.imageio.ImageIO;
import java.io.File;
import java.nio.file.Files;

public class ControllerTest {
	private Controller controller = new Controller();
    private File path = new File("./output");

    @Test
    public void sendPhoto() {
        Assertions.assertNotNull(controller);
        Assertions.assertTrue(controller.sendPhoto() instanceof ImageIO);
    }

    @Test
    public void capturePhoto() {
        Assertions.assertNotNull(controller);
        Assertions.assertTrue(controller.sendPhoto() instanceof ImageIO);
    }

    @Test
    public void savePhoto() {
        Assertions.assertNotNull(controller);
        Assertions.assertTrue(Files.exists(path.toPath()));
    }
}