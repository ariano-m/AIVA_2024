public class User {
    private String name;
    private String username;
    private String mail;
    private String password;
    private boolean admin;

    public User(String name, String mail, String password, String username, boolean admin) {
    }

    public boolean login(String username, String password) {
        return false;
    }

    public User createUser(String name, String mail, String password, String username, boolean admin) {
        return null;
    }

    public User resetPassword(String mail, String modifiedPassword){
        return null;
    }

    public User delete (String mail) {
        return null;
    }


}
