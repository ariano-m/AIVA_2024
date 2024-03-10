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

    public void resetPassword(String modifiedPassword){

    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getMail() {
        return mail;
    }

    public void setMail(String mail) {
        this.mail = mail;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public boolean isAdmin() {
        return admin;
    }

    public void setAdmin(boolean admin) {
        this.admin = admin;
    }
}
