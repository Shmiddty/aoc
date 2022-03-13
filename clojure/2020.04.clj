(use '[io :rename {read-all yum debug dbg}])
(use '[clojure.string :only (split)])
(use '[clojure.set :only (difference)])

(def inp
  (->> (yum)
       (#(split % #"\n\n"))
       (map
         #(->> %
               (re-seq #"(\w{3}):(\S+)")
               (map rest)
               ))
       ))

(def ppfields (set ["byr" "iyr" "eyr" "hgt" "hcl" "ecl" "pid"])); "cid"])) ignore cid

(defn missingfields [fields]
  (->> fields
       (map first)
       (set)
       (difference ppfields)
       ))

; would something like this work? nope. it doesn't.
;(defn validate
;  (["byr"] (fn [val] (->> (int val) (#(and (>= 1920 %) (<= 2002 %))))))
;  (["iyr"] (fn [val] (->> (int val) (#(and (>= 2010 %) (<= 2020 %))))))
;  (["eyr"] (fn [val] (->> (int val) (#(and (>= 2020 %) (<= 2030 %))))))
;  )
;(println ((validate "byr") "2015"))

; There's gotta be a better way!
(def validator #"((byr):(19[2-9][0-9]|200[0-2]))|((iyr):(201[0-9]|2020))|((eyr):(202[0-9]|2030))|((hgt):((1[5-8][0-9]|19[0-3])cm|(59|6[0-9]|7[0-6])in))|((hcl):\#[0-9a-f]{6})|((ecl):(amb|blu|brn|gry|grn|hzl|oth))|((pid):(\d{9})$)")
(defn validfields [fields]
  (->> fields
       (filter #(re-find validator (str (first %) ":" (second %))))
       ))

(->> inp
     (map missingfields)
     (filter #(= 0 (count %)))
     ;(filter #(or (and (= 1 (count %)) (contains? % "cid")) (= 0 (count %))))
     (count)
     (println)
     )

(->> inp
     (map validfields)
     (map missingfields)
     (filter #(= 0 (count %)))
     (count)
     (println)
     )

