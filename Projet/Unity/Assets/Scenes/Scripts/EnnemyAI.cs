using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class EnnemyAI : MonoBehaviour {
	// Create public variables for player speed, and for the Text UI game objects
    public PlayerStats Target;
    public EnnemyStats ennemyStats;
    public EnnemyBar ennemyBar;

    private float Distance;
    private float attackTime = 1;
    private float ennemy_speed = 5;    
    private float attackRange = 2.2f;
    private float attackRepeatTime = 1;
    private float Damping = 6;
    private float TheDammage = 20;

	// At the start of the game..
	void Start ()
	{
        attackTime = Time.time;
        ennemyBar.SetMaxValue(ennemyStats.getHealth());
    }

	// Each physics step..
	void Update ()
	{
        if(Target.getHealth() > 0)
        {
            Distance = Vector3.Distance(Target.transform.position, transform.position);

            lookAt();
            setHealthBar();

            if(Distance < attackRange){
                attack();
            }

            else{
                chase();
            }
        }
    }

    void chase()
    {
        transform.position = Vector3.MoveTowards(transform.position, Target.transform.position, ennemy_speed * Time.deltaTime);
    }

    void lookAt()
    {
        Quaternion rotation = Quaternion.LookRotation(Target.transform.position - transform.position);
        transform.rotation = Quaternion.Slerp(transform.rotation, rotation, Time.deltaTime * Damping);
    }

    void attack()
    {
        if (Time.time > attackTime){
            Target.ApplyDammage(TheDammage);
            attackTime = Time.time + attackRepeatTime;
        }
    }

    void setHealthBar(){
        ennemyBar.SetValue(ennemyStats.getHealth());
    }
}