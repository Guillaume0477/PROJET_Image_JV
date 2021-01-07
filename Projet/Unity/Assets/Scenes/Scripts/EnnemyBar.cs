using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class EnnemyBar : MonoBehaviour 
{
    public Slider slider;

    public void SetMaxValue(int maxValue)
    {
        slider.maxValue = maxValue;
        slider.value = maxValue;
    }

    public void SetValue(int value)
    {
        slider.value = value;
    }
}