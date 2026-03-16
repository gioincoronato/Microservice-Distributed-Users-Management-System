import java.util.Hashtable;

import javax.jms.*;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;

public class NotificationService {
    public static void main(String[] args) {
        System.out.println("NS running");

        Hashtable<String, String> env = new Hashtable<>();
        env.put(Context.INITIAL_CONTEXT_FACTORY, "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        env.put(Context.PROVIDER_URL, "tcp://activemq:61616");
        try{
            Context ctx = new InitialContext(env);

            ConnectionFactory factory = (ConnectionFactory) ctx.lookup("ConnectionFactory");
            Destination dest_recv = (Destination) ctx.lookup("dynamicQueues/notifyservice");

            Connection conn = factory.createConnection();
            
            Session session = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);
            MessageConsumer cons = session.createConsumer(dest_recv);

            cons.setMessageListener(new MessageListener() {
                @Override
                public void onMessage(Message m){
                    try{
                        if(m instanceof TextMessage){
                            TextMessage msg_in = (TextMessage)m;
                            String msg_txt = msg_in.getText();
                            System.out.println(msg_txt);
                        }
                    }catch(JMSException e){
                        e.printStackTrace();
                    }

                }
            }); 
            conn.start();
            while(true){
                Thread.sleep(1000);
            }
        }catch(NamingException | JMSException |InterruptedException e){
            e.printStackTrace();
        }

    }
    
}
