(ns util)

(defn untilrepeat [f [state & prev]]
  (if (= state (first prev))
      state
      (untilrepeat f (apply conj [(f state)] state prev))
      ))

