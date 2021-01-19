using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;


public class ShockWaveTutorial : MonoBehaviour
{
    private Vector3 incrementScale = new Vector3(10, 10, 10);
    private float ennemyDamage = 0;
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        if (transform.localScale.x <= 20){
            transform.localScale += Time.deltaTime*incrementScale;
        } 
        else {
            Destroy(gameObject);
        }
    }

    public float getEnnemyDamage()
    {
        return(ennemyDamage);
    }
    public void setEnnemyDamage(float manaD)
    {
        ennemyDamage = manaD;
    }
}