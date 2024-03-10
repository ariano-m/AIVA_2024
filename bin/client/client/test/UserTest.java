import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;


public class UserTest {
    private User user = new User("name","mail@ia.com", "password","nick",true);
    private String modifiedPassword = "1234";

    @Test
    public void loginTest() {
        Assertions.assertTrue(user.getUsername().equals("nick"));
        Assertions.assertTrue(user.getPassword().equals("password"));
    }

    @Test
    public void createUserTest() {
        User user1 = user.createUser("name","mail@ia.com", "password","nick",true);
        Assertions.assertNotNull(user);
        Assertions.assertTrue(user1 instanceof User);
    }

    @Test
    public void resetPasswordTest(){
        String oldPassword = user.getPassword();
        user.resetPassword(modifiedPassword);
        String newpassword = user.getPassword();
        Assertions.assertNotEquals(oldPassword, newpassword);
    }
}
