using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class EnnemyAI : MonoBehaviour {
	// Create public variables for player speed, and for the Text UI game objects
    public Transform Target;
    public float ennemy_speed = 5;    
    public float attackRange = 2.2f;
    public float attackRepeatTime = 1;
    public int TheDammage = 10;
    public float Damping = 6;

    private float Distance;
    private float attackTime = 1;


	// At the start of the game..
	void Start ()
	{
        attackTime = Time.time;
    }

	// Each physics step..
	void Update ()
	{
        Distance = Vector3.Distance(Target.position, transform.position);

        lookAt();

        if(Distance < attackRange){
            attack();
        }

        else{
            chase();
        }
    }

    void chase()
    {
        transform.position = Vector3.MoveTowards(transform.position, Target.position, ennemy_speed * Time.deltaTime);
    }

    void lookAt()
    {
        Quaternion rotation = Quaternion.LookRotation(Target.position - transform.position);
        transform.rotation = Quaternion.Slerp(transform.rotation, rotation, Time.deltaTime * Damping);
    }

    void attack()
    {
        if (Time.time > attackTime){
            Target.SendMessage("ApplyDammage", TheDammage);
            attackTime = Time.time + attackRepeatTime;
        }
    }
}